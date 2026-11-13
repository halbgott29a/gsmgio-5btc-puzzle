import hashlib, itertools, re, sys, time
from Crypto.Cipher import AES
src=open('hints_all.py').read().split("bases=set()")[0]
exec(src)     # defines P, variants, BL (salt,ct) ...
A7=["matrixsumlist","lastwordsbeforearchichoice","thispassword","sha256","ourfirsthintisyourlastcommand","enter","anstoo","ans","yinyang","yellowblueprimes","primes","dbbi","faed"]
bases=set()
for p in P: bases|=variants(p)
for k in (1,2,3):
    for perm in itertools.permutations(A7[:9],k):
        for sep in ("", " "): bases.add(sep.join(perm))
bases=sorted(bases); print("bases",len(bases),file=sys.stderr)
sh=lambda b: hashlib.sha256(b).hexdigest().encode()
pws=[]
for s in bases:
    b=s.encode(); pws.append(b); pws.append(sh(b))
pws=list(dict.fromkeys(pws)); print("passwords",len(pws),file=sys.stderr)
def evp(pw,salt,md,n):
    d=b"";pr=b""
    while len(d)<n: pr=md(pr+pw+salt).digest(); d+=pr
    return d[:n]
def chk(key,iv,tag,label,ct):
    pv=ct[-32:-16] if len(ct)>=32 else iv
    pl=AES.new(key,AES.MODE_CBC,pv).decrypt(ct[-16:]); p=pl[-1]
    if 1<=p<=16 and pl[-p:]==bytes([p])*p:
        full=AES.new(key,AES.MODE_CBC,iv).decrypt(ct); p=full[-1]; body=full[:-p]
        if len(body) and sum(1 for c in body if 32<=c<127 or c in(9,10,13))/len(body)>.85:
            print("HIT",tag,label,body[:300]); return 1
    return 0
hits=0;n=0;t0=time.time()
CIPH=((32,"aes256"),(24,"aes192"),(16,"aes128"))
# 1) EVP_BytesToKey variants
for pw in pws:
    for tag,(salt,ct) in BL.items():
        for mn,md in (("md5",hashlib.md5),("sha1",hashlib.sha1),("sha256",hashlib.sha256),("sha512",hashlib.sha512)):
            for kl,cn in CIPH:
                d=evp(pw,salt,md,kl+16); n+=1
                hits+=chk(d[:kl],d[kl:kl+16],tag,f"evp-{mn}-{cn}:{pw[:50]!r}",ct)
print("evp done",n,round(time.time()-t0),"s hits",hits,file=sys.stderr)
# 2) PBKDF2 (openssl -pbkdf2, 10000 iterations) 
for pw in pws:
    for tag,(salt,ct) in BL.items():
        for dn in ("sha256","sha1","sha512"):
            d=hashlib.pbkdf2_hmac(dn,pw,salt,10000,48)
            for kl,cn in CIPH:
                n+=1; hits+=chk(d[:kl],d[kl:kl+16],tag,f"pbkdf2-{dn}-{cn}:{pw[:50]!r}",ct)
print("total tests",n,"hits",hits,round(time.time()-t0),"s")
