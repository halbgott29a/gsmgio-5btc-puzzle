import base64, hashlib, itertools, re, sys
from Crypto.Cipher import AES

W = r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
def load(p):
    b = base64.b64decode("".join(open(p).read().split()))
    assert b[:8] == b"Salted__"
    return b[8:16], b[16:]
BLOBS = {"SALPH": load(W + r"\salphaseion_blob.txt"), "COSMIC": load(W + r"\cosmic_blob.txt")}
print({k: len(v[1]) for k, v in BLOBS.items()}, file=sys.stderr)

def evp(pw, salt, md):
    d = b""; pr = b""
    while len(d) < 48:
        pr = md(pr + pw + salt).digest(); d += pr
    return d[:32], d[32:48]

def good(pt):
    p = pt[-1]
    if not (1 <= p <= 16 and pt[-p:] == bytes([p]) * p): return None
    b = pt[:-p]
    if len(b) and sum(1 for c in b if 32 <= c < 127 or c in (9, 10, 13)) / len(b) > 0.85: return b
    return None

phrases = [
 "Happy new year! Make the best of everything. Oh, and here's a \"hint\" <3.",
 "Happy new year! Make the best of everything. Oh, and here's a hint <3.",
 "Happy new year! Make the best of everything. Oh, and here's a  \"hint\" <3.",
 "Happy new year", "Make the best of everything", "hint",
 "My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do.",
 "My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do",
 "My close friends have the best chance of solving it",
 "my close friends", "close friends", "NOTE: that is a hint.", "that is a hint",
 "Oh... and before I fall asleep. I want to assume it is quite clear I held quite a secret in my head which I seriously wanted to share with the planet... for those who can understand what I meant...",
 "I held quite a secret in my head which I seriously wanted to share with the planet",
 "The \"5\" btc was never the actual prize. That was only a tiny fraction.",
 "The 5 btc was never the actual prize. That was only a tiny fraction.",
 "5 btc was never the actual prize", "tiny fraction", "secret", "the planet",
 "EO11110", "11110", "Executive Order 11110", "5binary", "fefefe", "42", "101010",
 "1 2 3 4 5", "12345", ". .. ... .... .....",
]
cands = set()
for p in phrases:
    vs = {p, p.lower(), p.upper(), re.sub(r"[^A-Za-z0-9]", "", p), re.sub(r"[^A-Za-z0-9]", "", p).lower(),
          re.sub(r"[^A-Za-z0-9]", "", p).upper(), re.sub(r"\s+", "", p), p.strip(".!")}
    cands |= vs
# combos of pairs of short ones
short = [p for p in phrases if len(p) < 60]
for a, b in itertools.permutations(short, 2):
    cands.add(a + b); cands.add(re.sub(r"[^a-z0-9]", "", (a + b).lower()))

n = 0; hits = 0
for s in cands:
    forms = {s, hashlib.sha256(s.encode()).hexdigest(), hashlib.sha256(s.encode()).hexdigest().upper()}
    # double hash
    forms.add(hashlib.sha256(hashlib.sha256(s.encode()).hexdigest().encode()).hexdigest())
    for f in forms:
        for mdn, md in (("sha256", hashlib.sha256), ("md5", hashlib.md5)):
            for tag, (salt, ct) in BLOBS.items():
                n += 1
                k, iv = evp(f.encode(), salt, md)
                b = good(AES.new(k, AES.MODE_CBC, iv).decrypt(ct))
                if b:
                    hits += 1; print("HIT", tag, mdn, repr(s)[:80], repr(f)[:50], b[:200])
print(f"bases={len(cands)} tests={n} hits={hits}")
