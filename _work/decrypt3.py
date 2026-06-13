#!/usr/bin/env python3
"""Focused attack: sha256 KDF only, refined clue interpretations."""
import base64, hashlib, itertools, sys
from Crypto.Cipher import AES

BLOB = base64.b64decode("".join(open("salphaseion_blob.txt").read().split()))
SALT, CT = BLOB[8:16], BLOB[16:]

def evp(pw, salt, kl=32, il=16):
    d=b"";pr=b""
    while len(d)<kl+il:
        pr=hashlib.sha256(pr+pw+salt).digest(); d+=pr
    return d[:kl], d[kl:kl+il]

def plausible(b):
    return b and sum(1 for c in b if 32<=c<127 or c in (9,10,13))/len(b)>0.85

HITS=[]
def test(pw,label):
    if isinstance(pw,str): pw=pw.encode()
    k,iv=evp(pw,SALT)
    pt=AES.new(k,AES.MODE_CBC,iv).decrypt(CT)
    pad=pt[-1]
    if 1<=pad<=16 and pt[-pad:]==bytes([pad])*pad and plausible(pt[:-pad]):
        HITS.append((label,pt[:-pad])); print(f"[+] HIT {label!r} -> {pt[:-pad]!r}")
        return True
    return False

ENTRY="89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"
clues=["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword",
       "sha256ourfirsthintisyourlastcommand","sha256anstoo"]

def H(s): return hashlib.sha256(s.encode()).hexdigest()

cands=[]
# entry hash interpretations
cands += [("entry",ENTRY),("sha256(entry)",H(ENTRY)),
          ("sha256(entryupper)",H(ENTRY.upper()))]
# each clue raw + hashed
for c in clues:
    cands += [("raw:"+c,c),("h:"+c,H(c))]
# ordered concatenations of all clues
order=clues
joined="".join(order)
cands += [("joinall",joined),("h(joinall)",H(joined))]
# permutations of the 4 "noun" clues
nouns=["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword"]
for p in itertools.permutations(nouns):
    s="".join(p); cands += [("perm:"+s[:20],s),("h:perm:"+s[:20],H(s))]
# "first hint is your last command" => first clue + entry hash, hashed
cands += [("matrixsumlist+entry",H("matrixsumlist"+ENTRY)),
          ("entry+matrixsumlist",H(ENTRY+"matrixsumlist")),
          ("lastwords+entry",H("lastwordsbeforearchichoice"+ENTRY))]
# the two abba words combined ("matrixsumlist" then "enter")
cands += [("matrixsumlistenter",H("matrixsumlistenter")),
          ("raw:matrixsumlistenter","matrixsumlistenter")]

n=0
for lbl,pw in cands:
    n+=1; test(pw,lbl)
print(f"[*] sha256-KDF, tried {n}; hits={len(HITS)}", file=sys.stderr)
