#!/usr/bin/env python3
"""dbbi (91, a-i=1-9) combined with the 91-char phase-3.2.2 plaintext.
Test every result string as the SalPhaseIon AES password and for readability."""
import base64, hashlib, re
from Crypto.Cipher import AES

dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
P1="INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
assert len(dbbi)==len(P1)==91
D=[ "abcdefghi".index(c)+1 for c in dbbi ]   # 1..9

def is_prime(n): return n>1 and all(n%k for k in range(2,int(n**.5)+1))

BLOB=base64.b64decode("".join(open("salphaseion_blob.txt").read().split()))
SALT,CT=BLOB[8:16],BLOB[16:]
def evp(pw,kl=32,il=16):
    d=b"";pr=b""
    while len(d)<kl+il: pr=hashlib.sha256(pr+pw+SALT).digest(); d+=pr
    return d[:kl],d[kl:kl+il]
def aes_try(s):
    for pw in (s.encode(), s.upper().encode(), s.lower().encode(),
               hashlib.sha256(s.encode()).hexdigest().encode()):
        k,iv=evp(pw); pt=AES.new(k,AES.MODE_CBC,iv).decrypt(CT)
        p=pt[-1]
        if 1<=p<=16 and pt[-p:]==bytes([p])*p:
            b=pt[:-p]
            if b and sum(1 for c in b if 32<=c<127)/len(b)>0.85: return b
    return None

def readable(s):
    s=s.upper()
    common=("THE","AND","KEY","PRIVATE","PASS","YOUR","YOU","HALF","PRIME","MATRIX","GSMG","BTC","DOOR","ENTER")
    return sum(w in s for w in common)

results={}
def add(label,s):
    results[label]=s
    b=aes_try(s)
    if b: print(f"[+] AES HIT [{label}] pw={s!r}\n    -> {b!r}")
    r=readable(s)
    if r>=2: print(f"[~] readable({r}) [{label}]: {s}")

A=lambda i:ord(P1[i])-65
# combination operations
add("add",        "".join(chr((A(i)+D[i])%26+65) for i in range(91)))
add("sub",        "".join(chr((A(i)-D[i])%26+65) for i in range(91)))
add("beaufort",   "".join(chr((D[i]-A(i))%26+65) for i in range(91)))
add("add0",       "".join(chr((A(i)+D[i]-1)%26+65) for i in range(91)))
add("sub0",       "".join(chr((A(i)-D[i]+1)%26+65) for i in range(91)))
# zero-out selections
add("keep_prime_d","".join(P1[i] for i in range(91) if is_prime(D[i])))
add("keep_nonprime_d","".join(P1[i] for i in range(91) if not is_prime(D[i])))
add("keep_b",     "".join(P1[i] for i in range(91) if dbbi[i]=='b'))
add("keep_nonb",  "".join(P1[i] for i in range(91) if dbbi[i]!='b'))
add("keep_pos_prime","".join(P1[i] for i in range(91) if is_prime(i+1)))
add("keep_d_eq_a","".join(P1[i] for i in range(91) if dbbi[i]=='a'))
add("keep_d_in_ab","".join(P1[i] for i in range(91) if dbbi[i] in 'ab'))
# dbbi selects P1 index (value as pointer)
add("d_as_index", "".join(P1[D[i]-1] for i in range(91)))
# P1 selects dbbi
# multiply positions etc
add("keep_even_d","".join(P1[i] for i in range(91) if D[i]%2==0))
add("keep_odd_d", "".join(P1[i] for i in range(91) if D[i]%2==1))

# show a few raw outputs
print("\n--- sample outputs ---")
for k in ("add","sub","beaufort","keep_prime_d","keep_b","keep_nonb","keep_pos_prime"):
    print(f"{k:16}: {results[k]}")
print(f"\ntotal ops={len(results)}")
