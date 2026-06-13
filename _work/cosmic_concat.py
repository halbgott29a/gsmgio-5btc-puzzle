#!/usr/bin/env python3
"""Cosmic Duality: try SHA256(concatenation of known SalPhaseIon clues) as the
openssl password, matching the puzzle's established multi-part pattern.
Permutations + subsets, raw and hashed, with optional separators."""
import base64, hashlib, itertools
from Crypto.Cipher import AES

def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
COS=load(r"D:\tmp\gsmgio-5btc-puzzle\ChatExport\files\cd.b64.txt")
SAL=load("salphaseion_blob.txt")
def evp(pw,salt,kl=32,il=16):
    d=b"";pr=b""
    while len(d)<kl+il: pr=hashlib.sha256(pr+pw+salt).digest();d+=pr
    return d[:kl],d[kl:kl+il]
def good(pt):
    p=pt[-1]
    if 1<=p<=16 and pt[-p:]==bytes([p])*p:
        b=pt[:-p]
        if b and sum(1 for c in b if 32<=c<127 or c in(9,10,13))/len(b)>0.85: return b
    return None
def test(pwstr):
    for f in {pwstr, hashlib.sha256(pwstr.encode()).hexdigest(),
              hashlib.sha256(pwstr.upper().encode()).hexdigest()}:
        for tag,(salt,ct) in (("COSMIC",COS),("SALPH",SAL)):
            b=good(AES.new(*(lambda kv:(kv[0],AES.MODE_CBC,kv[1]))(evp(f.encode(),salt))).decrypt(ct)) \
              if False else None
    # simpler explicit loop:
    for f in {pwstr, hashlib.sha256(pwstr.encode()).hexdigest(),
              hashlib.sha256(pwstr.upper().encode()).hexdigest()}:
        for tag,(salt,ct) in (("COSMIC",COS),("SALPH",SAL)):
            k,iv=evp(f.encode(),salt)
            b=good(AES.new(k,AES.MODE_CBC,iv).decrypt(ct))
            if b:
                print(f"[+++ {tag}] base={pwstr[:50]!r} form={f[:24]!r}\n   -> {b[:200]!r}")
                return True
    return False

clues=["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword","yinyang"]
seps=["","",]  # join with empty (puzzle style aBa connected)
n=0;hits=0
# all subset permutations of size 2..5
for r in range(2,6):
    for perm in itertools.permutations(clues,r):
        for sep in ("","-"," "):
            s=sep.join(perm)
            n+=1
            if test(s): hits+=1
# also single clues already tried but include capitalized variants per puzzle (aBa)
for c in clues:
    if test(c): hits+=1
print(f"[*] tried {n} concatenations; hits={hits}")
