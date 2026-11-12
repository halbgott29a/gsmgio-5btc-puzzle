import base64, hashlib, re, sys, time
from Crypto.Cipher import AES
W=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
md=open(r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle\unverified\phase3.2_1141.md",encoding='utf8').read()
s=re.search(r"s='(yourlife[a-z']+)'",md).group(1)
print("text len",len(s),file=sys.stderr)
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
BL={"SALPH":load(W+r"\salphaseion_blob.txt"),"COSMIC":load(W+r"\cosmic_blob.txt")}
sha=hashlib.sha256
def kiv(pw,salt):
    a=sha(pw+salt).digest(); b=sha(a+pw+salt).digest(); c=sha(b+pw+salt).digest()
    d=a+b+c; return d[:32],d[32:48]
tails={t:(salt,ct,ct[-32:-16],ct[-16:]) for t,(salt,ct) in BL.items()}
def test(pw,label):
    for t,(salt,ct,pv,last) in tails.items():
        k,iv=kiv(pw,salt)
        pl=AES.new(k,AES.MODE_CBC,pv).decrypt(last); p=pl[-1]
        if 1<=p<=16 and pl[-p:]==bytes([p])*p:
            full=AES.new(k,AES.MODE_CBC,iv).decrypt(ct); p=full[-1]
            body=full[:-p]
            if sum(1 for c in body if 32<=c<127 or c in(9,10,13))/max(1,len(body))>.85:
                print("HIT",t,label,body[:200]); return True
    return False
t0=time.time(); n=0; seen=set()
MAXL=int(sys.argv[1]) if len(sys.argv)>1 else 250
for i in range(len(s)):
    for j in range(i+3,min(len(s),i+MAXL)+1):
        sub=s[i:j]
        if sub in seen: continue
        seen.add(sub)
        b=sub.encode()
        test(b,f"raw[{i}:{j}]"); test(sha(b).hexdigest().encode(),f"sha[{i}:{j}]"); n+=2
    if i%200==0: print(i,n,round(time.time()-t0),file=sys.stderr)
print("done",n,"tests",round(time.time()-t0),"s")
