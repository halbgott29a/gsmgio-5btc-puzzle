#!/usr/bin/env python3
"""Attack the Cosmic Duality AES blob with passwords derived from every decoded
SalPhaseIon / creator-hint clue. Tests raw/upper/lower/sha256-hex forms, sha256
& md5 KDF, against both the Cosmic Duality and SalPhaseIon blobs."""
import base64, hashlib, itertools, re
from Crypto.Cipher import AES

def load(path):
    b=base64.b64decode("".join(open(path).read().split()))
    assert b[:8]==b"Salted__", path
    return b[8:16], b[16:]
COS_SALT,COS_CT = load(r"D:\tmp\gsmgio-5btc-puzzle\ChatExport\files\cd.b64.txt")
SAL_SALT,SAL_CT = load("salphaseion_blob.txt")
print(f"cosmic ct={len(COS_CT)}B salt={COS_SALT.hex()}")

def evp(pw,salt,md,kl=32,il=16):
    d=b"";pr=b""
    while len(d)<kl+il: pr=md(pr+pw+salt).digest(); d+=pr
    return d[:kl],d[kl:kl+il]
def good(pt):
    if len(pt)<1: return None
    p=pt[-1]
    if not (1<=p<=16 and pt[-p:]==bytes([p])*p): return None
    b=pt[:-p]
    if b and sum(1 for c in b if 32<=c<127 or c in(9,10,13))/len(b)>0.85: return b
    return None
def try_all(pwstr):
    forms={pwstr,pwstr.upper(),pwstr.lower(),
           hashlib.sha256(pwstr.encode()).hexdigest(),
           hashlib.sha256(pwstr.upper().encode()).hexdigest(),
           hashlib.sha256(pwstr.encode()).digest().hex()}
    for f in forms:
        pw=f.encode()
        for mdn,md in (("sha256",hashlib.sha256),("md5",hashlib.md5)):
            for tag,(salt,ct) in (("COSMIC",(COS_SALT,COS_CT)),("SALPH",(SAL_SALT,SAL_CT))):
                k,iv=evp(pw,salt,md)
                b=good(AES.new(k,AES.MODE_CBC,iv).decrypt(ct))
                if b:
                    print(f"[+++ HIT {tag}] base={pwstr!r} form={f[:40]!r} md={mdn}\n     -> {b[:200]!r}")
                    return True
    return False

# ---- candidate base strings ----
clues=["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword",
 "yinyang","yin yang","cosmicduality","cosmic duality","salphaseion","salphaseon",
 "thematrixhasyou","causality","theseedisplanted","HASHTHETEXT","keymaker",
 "yellowblueprimes","primes","architect","neo","themerovingian","merovingian"]
creator_hint="yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised"
big=[creator_hint,
 "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE",
 "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"]

bases=set(clues)|set(big)
# pairwise concat of short clues
for a,b in itertools.product(clues,clues):
    if len(a)+len(b)<=60: bases.add(a+b)
# the established 7-part style: sha256 of concatenations
print(f"[*] testing {len(bases)} base strings x many forms...")
found=0
for s in bases:
    if try_all(s): found+=1
print(f"[*] done. hits={found}")
