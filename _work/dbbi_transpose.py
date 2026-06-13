#!/usr/bin/env python3
"""Transposition attack: reorder dbbi/INCASE via permutations derived from each
other, and via 7x13/13x7 grids. Decode dbbi-results as digits->ASCII; score
INCASE-results as English; test everything as the SalPhaseIon AES password."""
import base64, hashlib, re
from Crypto.Cipher import AES

dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
P1  ="INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
N=91
BLOB=base64.b64decode("".join(open("salphaseion_blob.txt").read().split()))
SALT,CT=BLOB[8:16],BLOB[16:]
def evp(pw,kl=32,il=16):
    d=b"";pr=b""
    while len(d)<kl+il: pr=hashlib.sha256(pr+pw+SALT).digest();d+=pr
    return d[:kl],d[kl:kl+il]
def aes_try(s):
    for c in {s,s.upper(),s.lower(),hashlib.sha256(s.encode()).hexdigest()}:
        if not c: continue
        k,iv=evp(c.encode());pt=AES.new(k,AES.MODE_CBC,iv).decrypt(CT);p=pt[-1]
        if 1<=p<=16 and pt[-p:]==bytes([p])*p:
            b=pt[:-p]
            if b and sum(1 for ch in b if 32<=ch<127)/len(b)>0.85: return c,b
    return None

WORDS={w for w in "THE AND KEY PRIVATE PASSWORD PUZZLE MATRIX PRIME ENTER DOOR HALF BETTER YELLOW BLUE YINYANG CRACK BITCOIN GIVE AWAY FRONT EYES LAST STEP TRUE GSMG BELONG FUNDS LIVE NEED ALSO YOUR THAT WITH THIS HAVE WIF KEYNOTE SOURCE CODE".split() if len(w)>=3}
def eng(s):
    s=s.upper();return sum(len(w)*s.count(w) for w in WORDS)

DIGMAPS={"a1i9o0":{**{c:str(i+1) for i,c in enumerate('abcdefghi')},'o':'0'},
         "a0i8":{c:str(i) for i,c in enumerate('abcdefghi')}}
def to_digits(s,mp): return "".join(mp.get(c,'') for c in s)
def ascii_from_digits(ds,bs):
    out=[];ok=0
    for i in range(0,len(ds)-bs+1,bs):
        try:
            v=int(ds[i:i+bs])
        except: continue
        if 32<=v<=126: out.append(chr(v));ok+=1
        else: out.append('·')
    return "".join(out),ok

HITS=[]; CAND=[]   # (score, label, display, aes_payload_string)
def reg_dbbi(label,s):     # s is an a-i string -> try digit->ascii
    a=aes_try(s)
    if a: HITS.append((label,s,a)); print(f"[+++ AES] {label} pw={a[0]!r} -> {a[1]!r}")
    for mn,mp in DIGMAPS.items():
        ds=to_digits(s,mp)
        for bs in (2,3):
            txt,ok=ascii_from_digits(ds,bs)
            if ok>=8:
                sc=eng(txt)+ok
                CAND.append((sc,f"{label}/{mn}/a{bs}",txt))
                a=aes_try(txt.replace('·',''))
                if a: HITS.append((label+"/ascii",txt,a)); print(f"[+++ AES] {label}/ascii pw={a[0]!r}")
def reg_eng(label,s):      # s is A-Z english candidate
    CAND.append((eng(s),label,s))
    a=aes_try(s)
    if a: HITS.append((label,s,a)); print(f"[+++ AES] {label} pw={a[0]!r} -> {a[1]!r}")

# ---------- permutations ----------
def argsort_stable(keys): return sorted(range(N), key=lambda i:(keys[i],i))
def apply_perm(s,perm): return "".join(s[p] for p in perm)
def inv(perm):
    r=[0]*N
    for i,p in enumerate(perm): r[p]=i
    return r

inc_keys=[ord(c) for c in P1]
dbi_vals=[ "abcdefghi".index(c) for c in dbbi ]
perm_inc=argsort_stable(inc_keys)         # order positions by INCASE letter
perm_dbi=argsort_stable(dbi_vals)         # order positions by dbbi value

for pname,perm in (("byINCASE",perm_inc),("byINCASEinv",inv(perm_inc)),
                   ("byDBBI",perm_dbi),("byDBBIinv",inv(perm_dbi))):
    reg_dbbi(f"dbbi_{pname}", apply_perm(dbbi,perm))
    reg_dbbi(f"dbbiR_{pname}", apply_perm(dbbi[::-1],perm))
    reg_eng(f"INCASE_{pname}", apply_perm(P1,perm))

# ---------- grid transpositions on dbbi ----------
def grid_read(s,r,c,mode):
    g=[list(s[i*c:(i+1)*c]) for i in range(r)]
    if mode=="cols": return "".join(g[i][j] for j in range(c) for i in range(r))
    if mode=="colsR": return "".join(g[i][j] for j in range(c) for i in range(r-1,-1,-1))
    if mode=="rowsR": return "".join("".join(row[::-1]) for row in g)
    if mode=="boust":  # boustrophedon columns
        out=[]
        for j in range(c):
            rng=range(r) if j%2==0 else range(r-1,-1,-1)
            for i in rng: out.append(g[i][j])
        return "".join(out)
    return s
for (r,c) in ((7,13),(13,7)):
    for mode in ("cols","colsR","rowsR","boust"):
        reg_dbbi(f"grid{r}x{c}_{mode}", grid_read(dbbi,r,c,mode))
        reg_dbbi(f"grid{r}x{c}_{mode}_R", grid_read(dbbi[::-1],r,c,mode))

CAND.sort(reverse=True)
with open("dbbi_transpose_out.txt","w",encoding="utf-8") as f:
    f.write(f"AES hits: {len(HITS)}\n\nTOP 30 candidates:\n")
    for sc,l,s in CAND[:30]:
        f.write(f"[{sc:4d}] {l:26} {s}\n")
print(f"\nAES hits={len(HITS)}; candidates={len(CAND)}; see dbbi_transpose_out.txt")
print("TOP 10:")
for sc,l,s in CAND[:10]:
    print(f"  [{sc:4d}] {l:24} {s[:60]}")
