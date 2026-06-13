#!/usr/bin/env python3
"""Exhaustive dbbi (x) INCASE attack. Both 91 chars.
Tries all sign/order/mapping combos of classical poly-alpha ciphers, plus
selection/zeroing schemes. Scores each output for English-ness and tests it
as the SalPhaseIon AES password."""
import base64, hashlib, itertools, re
from Crypto.Cipher import AES

dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
P1  ="INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
assert len(dbbi)==len(P1)==91

# ---- AES ----
BLOB=base64.b64decode("".join(open("salphaseion_blob.txt").read().split()))
SALT,CT=BLOB[8:16],BLOB[16:]
def evp(pw,kl=32,il=16):
    d=b"";pr=b""
    while len(d)<kl+il: pr=hashlib.sha256(pr+pw+SALT).digest(); d+=pr
    return d[:kl],d[kl:kl+il]
def aes_try(s):
    cands={s, s.upper(), s.lower(), hashlib.sha256(s.encode()).hexdigest(),
           hashlib.sha256(s.upper().encode()).hexdigest()}
    for c in cands:
        k,iv=evp(c.encode()); pt=AES.new(k,AES.MODE_CBC,iv).decrypt(CT); p=pt[-1]
        if 1<=p<=16 and pt[-p:]==bytes([p])*p:
            b=pt[:-p]
            if b and sum(1 for ch in b if 32<=ch<127)/len(b)>0.85: return c,b
    return None

# ---- English scorer (quadgram-ish via common words) ----
WORDS=set("""the and that have for not with you this but his from they say her she will one all would there their what out about who get which when make can like time just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most THE PRIVATE KEY PASSWORD PUZZLE MATRIX PRIME ENTER DOOR HALF BETTER YELLOW BLUE YIN YANG CRACK SALT BITCOIN ADDRESS WALLET SHA HASH GIVE AWAY FRONT EYES SEEING LAST STEP TRUE GSMG BELONG FUNDS LIVE NEED ALSO""".split())
WORDS={w.upper() for w in WORDS if len(w)>=3}
def eng_score(s):
    s=s.upper()
    sc=0
    for w in WORDS:
        if w in s: sc+=len(w)*s.count(w)
    # vowel sanity
    v=sum(s.count(c) for c in "AEIOU")/max(1,len(s))
    if v<0.25 or v>0.55: sc-=5
    return sc

def L2N(c): return ord(c)-65       # A->0
def N2L(n): return chr(n%26+65)

maps = {"a1i9":{c:i+1 for i,c in enumerate("abcdefghi")},
        "a0i8":{c:i   for i,c in enumerate("abcdefghi")}}

hits=[]; scored=[]
def consider(label,s):
    if not re.fullmatch(r'[A-Za-z0-9]+',s): return
    r=aes_try(s)
    if r: hits.append((label,s,r)); print(f"[+++] AES HIT [{label}] pw={r[0]!r}\n      -> {r[1]!r}")
    scored.append((eng_score(s),label,s))

# 1) polyalphabetic: treat dbbi as key K (values), P1 as text
for mname,mp in maps.items():
    K=[mp[c] for c in dbbi]
    P=[L2N(c) for c in P1]
    consider(f"vig+_{mname}",  "".join(N2L(P[i]+K[i]) for i in range(91)))
    consider(f"vig-_{mname}",  "".join(N2L(P[i]-K[i]) for i in range(91)))
    consider(f"beau_{mname}",  "".join(N2L(K[i]-P[i]) for i in range(91)))
# 2) treat dbbi letters AS letters (a=0..i=8 in A-Z space), INCASE as key -> decode dbbi
Dl=[L2N(c.upper()) for c in dbbi]   # a->0,b->1,...i->8
Pk=[L2N(c) for c in P1]
consider("Cdbbi-Kincase_sub", "".join(N2L(Dl[i]-Pk[i]) for i in range(91)))
consider("Cdbbi-Kincase_beau","".join(N2L(Pk[i]-Dl[i]) for i in range(91)))
consider("Cdbbi+Kincase_add", "".join(N2L(Dl[i]+Pk[i]) for i in range(91)))

# 3) selection / zeroing schemes (subsequences of INCASE)
def is_prime(n): return n>1 and all(n%k for k in range(2,int(n**.5)+1))
for mname,mp in maps.items():
    V=[mp[c] for c in dbbi]
    consider(f"keepPrimeVal_{mname}", "".join(P1[i] for i in range(91) if is_prime(V[i])))
    consider(f"dropPrimeVal_{mname}", "".join(P1[i] for i in range(91) if not is_prime(V[i])))
    for t in range(0,10):
        consider(f"keep_ge{t}_{mname}", "".join(P1[i] for i in range(91) if V[i]>=t))
        consider(f"keep_eq{t}_{mname}", "".join(P1[i] for i in range(91) if V[i]==t))
consider("keep_b",     "".join(P1[i] for i in range(91) if dbbi[i]=='b'))
consider("keep_nonb",  "".join(P1[i] for i in range(91) if dbbi[i]!='b'))
consider("keep_posprime","".join(P1[i] for i in range(91) if is_prime(i+1)))
consider("drop_posprime","".join(P1[i] for i in range(91) if not is_prime(i+1)))

# 4) digit arithmetic: dbbi digits with INCASE letter-number (A=1..Z=26) mod 10 etc -> as text
# (skip; covered by polyalpha)

scored.sort(reverse=True)
with open("dbbi_full_out.txt","w",encoding="utf-8") as f:
    f.write(f"AES hits: {len(hits)}\n\n=== TOP 25 by English score ===\n")
    for sc,lbl,s in scored[:25]:
        f.write(f"[{sc:4d}] {lbl:22} {s}\n")
print(f"\nAES hits={len(hits)}; candidates scored={len(scored)}; see dbbi_full_out.txt")
print("TOP 8:")
for sc,lbl,s in scored[:8]:
    print(f"  [{sc:4d}] {lbl:20} {s[:70]}")
