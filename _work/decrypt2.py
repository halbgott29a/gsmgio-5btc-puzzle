#!/usr/bin/env python3
"""Broader attack on the SalPhaseIon AES blob."""
import base64, hashlib, itertools, sys
from Crypto.Cipher import AES

BLOB = base64.b64decode("".join(open("salphaseion_blob.txt").read().split()))
SALT, CT = BLOB[8:16], BLOB[16:]

def evp(password, salt, md, klen=32, ivlen=16):
    d=b""; prev=b""
    while len(d)<klen+ivlen:
        prev=md(prev+password+salt).digest(); d+=prev
    return d[:klen], d[klen:klen+ivlen]

def plausible(b):
    if not b: return False
    return sum(1 for c in b if 32<=c<127 or c in (9,10,13))/len(b) > 0.85

HITS=[]
def test(pw, label):
    if isinstance(pw,str): pw=pw.encode()
    for mdn,md in (("md5",hashlib.md5),("sha256",hashlib.sha256)):
        k,iv=evp(pw,SALT,md)
        pt=AES.new(k,AES.MODE_CBC,iv).decrypt(CT)
        pad=pt[-1]
        if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad:
            body=pt[:-pad]
            if plausible(body):
                HITS.append((mdn,label,body))
                print(f"[+] HIT md={mdn} label={label!r}\n    -> {body!r}")

# ---- the original 14x14 matrix ----
MATRIX = """
0 0 1 1 0 1 0 0 1 0 1 1 0 0
1 1 1 1 0 0 1 1 1 0 1 0 1 1
1 1 0 1 1 1 0 1 0 0 1 0 0 1
0 1 1 0 1 0 0 0 0 1 1 1 0 1
0 1 1 0 0 0 1 1 0 0 0 1 1 0
1 0 0 1 1 0 0 0 1 0 0 0 1 1
1 0 0 1 1 1 0 0 0 1 0 0 0 0
1 1 1 0 0 0 0 0 0 0 1 0 0 0
0 0 0 1 1 1 0 1 1 1 1 1 0 1
1 1 1 1 1 1 0 0 1 1 0 0 0 1
1 1 0 1 0 0 0 0 0 1 1 0 1 1
1 1 1 1 0 0 1 0 1 0 1 1 0 0
0 1 0 1 1 1 0 1 0 0 0 1 1 0
0 1 1 0 1 1 0 1 1 0 1 0 1 1
"""
rows=[[int(x) for x in r.split()] for r in MATRIX.strip().splitlines()]
rowsums=[sum(r) for r in rows]
colsums=[sum(rows[i][j] for i in range(14)) for j in range(14)]
total=sum(rowsums)

matrix_strs = [
    "".join(map(str,rowsums)),
    "".join(map(str,colsums)),
    str(total),
    " ".join(map(str,rowsums)),
    "".join(str(b) for r in rows for b in r),   # full bitstring
]

CLUES = ["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword",
    "sha256ourfirsthintisyourlastcommand","sha256anstoo",
    "ourfirsthintisyourlastcommand","sha256","salphaseion","cosmicduality",
    "thematrixhasyou","causality","theseedisplanted","HASHTHETEXT",
    "matrixsumlistenter","entermatrixsumlist",
]

# Architect last words before the choice (Matrix Reloaded) - candidate phrases
ARCH = [
    "theproblemischoice", "choice", "hopeitisthequintessentialhumandelusion",
    "thedoortoyourright", "thedoortoyourleft", "concordantly",
]

def all_candidates():
    pool = CLUES + ARCH + matrix_strs
    for w in pool:
        yield "raw:"+w[:30], w
        yield "sha256hex:"+w[:30], hashlib.sha256(w.encode()).hexdigest()
        yield "sha256x2:"+w[:30], hashlib.sha256(hashlib.sha256(w.encode()).hexdigest().encode()).hexdigest()
    # pairwise concatenations of clues, hashed (matching puzzle pattern)
    for a,b in itertools.product(CLUES, CLUES):
        c=a+b
        yield "sha256hex:"+c[:25], hashlib.sha256(c.encode()).hexdigest()
        yield "raw:"+c[:25], c

n=0
for lbl,pw in all_candidates():
    n+=1; test(pw,lbl)
print(f"[*] matrix totals: rowsums={rowsums} total={total}", file=sys.stderr)
print(f"[*] tried {n}; hits={len(HITS)}", file=sys.stderr)
