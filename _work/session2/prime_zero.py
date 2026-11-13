import base64, hashlib, itertools, re, sys, binascii
from Crypto.Cipher import AES
W=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
raw=open(W+r"\salph_raw.txt").read().strip()
dbbi=raw[:91]; blob=raw[91:195]; faed=raw[195:765]; tail=raw[765:]
assert len(faed)==570 and faed.startswith("faedgg")
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
BL={"SALPH":load(W+r"\salphaseion_blob.txt"),"COSMIC":load(W+r"\cosmic_blob.txt")}
def evp(pw,salt,md):
    d=b"";pr=b""
    while len(d)<48: pr=md(pr+pw+salt).digest(); d+=pr
    return d[:32],d[32:48]
def good(pt):
    p=pt[-1]
    if not(1<=p<=16 and pt[-p:]==bytes([p])*p): return None
    b=pt[:-p]
    return b if len(b) and sum(1 for c in b if 32<=c<127 or c in(9,10,13))/len(b)>.85 else None
def oracle(pwbytes,label):
    out=False
    for md in (hashlib.sha256,hashlib.md5):
        for tag,(s,c) in BL.items():
            k,iv=evp(pwbytes,s,md); r=good(AES.new(k,AES.MODE_CBC,iv).decrypt(c))
            if r: print("AES HIT",tag,label,r[:150]); out=True
    return out
def primes(n):
    s=[1]*(n+1); s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=0
    return {i for i,v in enumerate(s) if v}
PR=primes(2000)
def pscore(b):
    if len(b)<4: return 0
    asc=sum(1 for x in b if 32<=x<127 or x in(9,10,13))/len(b)
    return asc
reports=[]
def check(label,bts):
    if not bts: return
    a=pscore(bts)
    flag = b"Salted__" in bts or (a>0.9 and len(bts)>=8) or re.search(rb"[A-Za-z ]{12,}",bts)
    if flag: reports.append((label,len(bts),round(a,2),bts[:60]))
    # also AES oracle on bytes and hex and sha256 of text
    oracle(bts,label+"|raw")
    oracle(hashlib.sha256(bts).hexdigest().encode(),label+"|sha256hex")
    oracle(bts.hex().encode(),label+"|hex")
def from_digits(ds,label):
    # ds = string of decimal digits
    if not ds.strip("0"): return
    n=int(ds)
    h=format(n,'x')
    for hh in (h,"0"+h):
        if len(hh)%2==0: check(label+"|dec->hex->bytes",binascii.a2b_hex(hh)); break
    # decimal ascii triples/pairs
    for k in (2,3):
        vals=[int(ds[i:i+k]) for i in range(0,len(ds)-k+1,k)]
        check(label+f"|dec{k}",bytes(v for v in vals if v<256) if all(v<256 for v in vals) else b"")
    # base10 -> bytes via n.to_bytes (same as hex) skip
bases={"dbbi":dbbi,"faed":faed,"dbbi+faed":dbbi+faed,"raw":raw[:765],"faed+dbbi":faed+dbbi,"blob?":None}
bases.pop("blob?")
maps={"a1":lambda c:str("abcdefghi".index(c)+1) if c in "abcdefghi" else "0",
      "a0":lambda c:str("abcdefghi".index(c)) if c in "abcdefghi" else "0"}
def zero_sets(L):
    idx=range(L)
    yield "none",set()
    for off in (0,1):
        P={i for i in idx if (i+off) in PR}
        yield f"prime@{off}",P
        yield f"nonprime@{off}",set(idx)-P
        yield f"prime@{off}+1?",set()  # placeholder no-op
    # primes mod structure: indices that are prime powers / squares
    yield "square",{i for i in idx if int(i**.5)**2==i}
n=0
for bn,s in bases.items():
    for mn,mf in maps.items():
        for zn,Z in zero_sets(len(s)):
            if zn.endswith("?"): continue
            # variant A: zero the chars at Z; variant B: delete chars at Z; variant C: keep only Z
            A="".join("0" if i in Z else mf(c) for i,c in enumerate(s))
            B="".join(mf(c) for i,c in enumerate(s) if i not in Z)
            C="".join(mf(c) for i,c in enumerate(s) if i in Z)
            for v,ds in (("zero",A),("del",B),("keep",C)):
                n+=1; from_digits(ds,f"{bn}/{mn}/{zn}/{v}")
                # same for string reversed
                from_digits(ds[::-1],f"{bn}/{mn}/{zn}/{v}/rev")
print("variants",n)
for r in reports: print(r)
