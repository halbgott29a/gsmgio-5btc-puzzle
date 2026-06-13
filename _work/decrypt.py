#!/usr/bin/env python3
"""
GSMG.IO 5BTC puzzle - SalPhaseIon AES blob attack.

Replicates OpenSSL `enc -aes-256-cbc -d -a -pass pass:<P>` for both the
historical default (EVP_BytesToKey with MD5) and modern (-md sha256),
trying many password derivations from the decoded SalPhaseIon clues.
"""
import base64, hashlib, itertools, sys

BLOB_B64 = open("salphaseion_blob.txt").read().split()
BLOB = base64.b64decode("".join(BLOB_B64))
assert BLOB[:8] == b"Salted__", BLOB[:8]
SALT = BLOB[8:16]
CT   = BLOB[16:]
print(f"[*] ciphertext bytes: {len(CT)}  salt={SALT.hex()}", file=sys.stderr)

def evp_bytes_to_key(password: bytes, salt: bytes, md, klen=32, ivlen=16):
    d = b""; prev = b""
    while len(d) < klen + ivlen:
        prev = md(prev + password + salt).digest()
        d += prev
    return d[:klen], d[klen:klen+ivlen]

def aes_cbc_decrypt(key, iv, ct):
    try:
        from Crypto.Cipher import AES
    except ImportError:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        c = Cipher(algorithms.AES(key), modes.CBC(iv))
        dec = c.decryptor()
        return dec.update(ct) + dec.finalize()
    return AES.new(key, AES.MODE_CBC, iv).decrypt(ct)

def try_pw(password: bytes, label: str):
    for mdname, md in (("md5", hashlib.md5), ("sha256", hashlib.sha256)):
        key, iv = evp_bytes_to_key(password, SALT, md)
        pt = aes_cbc_decrypt(key, iv, CT)
        # valid PKCS7 padding check
        pad = pt[-1]
        if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
            body = pt[:-pad]
            if is_plausible(body):
                print(f"[+] HIT md={mdname} pw={label!r} -> {body!r}")
                return True
    return False

def is_plausible(b: bytes) -> bool:
    if not b:
        return False
    printable = sum(1 for c in b if 32 <= c < 127 or c in (9,10,13))
    return printable / len(b) > 0.9

# ---- password candidate generators -----------------------------------
DERIVED = [
    "matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword",
    "shabefourfirsthintisyourlastcommand", "shabefanstoo",
    "ourfirsthintisyourlastcommand", "firsthintisyourlastcommand",
    "yourlastcommand", "salphaseion", "salphaselon", "cosmicduality",
    "thematrixhasyou", "causality",
]

# "first hint" from earliest stages / "last command" candidates
FIRST_HINTS = [
    "theseedisplanted", "gsmg.io/theseedisplanted",
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",
    "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
    "HASHTHETEXT",
]

def candidates():
    for w in DERIVED + FIRST_HINTS:
        yield w, w
        yield "sha256(%s)"%w, hashlib.sha256(w.encode()).hexdigest()
        yield "sha256_raw(%s)"%w, hashlib.sha256(w.encode()).digest()
    # combos hinted by "first hint is your last command" + "ans too"
    for a in DERIVED + FIRST_HINTS:
        for b in DERIVED + FIRST_HINTS:
            combo = a + b
            yield combo, combo
            yield "sha256(%s)"%combo, hashlib.sha256(combo.encode()).hexdigest()

def main():
    n = 0
    found = False
    for label, pw in candidates():
        n += 1
        if isinstance(pw, str):
            pw = pw.encode()
        if try_pw(pw, label):
            found = True
    print(f"[*] tried {n} candidates. found={found}", file=sys.stderr)

if __name__ == "__main__":
    main()
