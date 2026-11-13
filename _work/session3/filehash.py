import base64, hashlib, os, sys
from Crypto.Cipher import AES
W=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
BL={"SALPH":load(W+r"\salphaseion_blob.txt"),"COSMIC":load(W+r"\cosmic_blob.txt")}
sha=hashlib.sha256
def kiv(pw,salt):
    a=sha(pw+salt).digest(); b=sha(a+pw+salt).digest(); c=sha(b+pw+salt).digest(); d=a+b+c; return d[:32],d[32:48]
T={t:(s,ct,ct[-32:-16],ct[-16:]) for t,(s,ct) in BL.items()}
def test(pw,label):
    for t,(salt,ct,pv,last) in T.items():
        k,iv=kiv(pw,salt); pl=AES.new(k,AES.MODE_CBC,pv).decrypt(last); p=pl[-1]
        if 1<=p<=16 and pl[-p:]==bytes([p])*p:
            full=AES.new(k,AES.MODE_CBC,iv).decrypt(ct); p=full[-1]; body=full[:-p]
            if sum(1 for c in body if 32<=c<127 or c in(9,10,13))/max(1,len(body))>.85:
                print("HIT",t,label,body[:300]); return True
files=[]
for root in (r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle",r"D:\project_python\gsmgio-puzzle\halbgott29a-fork",
             r"C:\Users\edu4g\AppData\Local\Temp\claude\abf65afab48cd543\cf7da61d-d3c6-4cbc-be17-847e53fcb4f1\scratchpad\salph"):
    for d,ds,fs in os.walk(root):
        if ".git" in d.split(os.sep) or "_work" in d.split(os.sep): continue
        for f in fs:
            p=os.path.join(d,f)
            if os.path.getsize(p)<20_000_000: files.append(p)
print(len(files),"files",file=sys.stderr)
algos={"sha256":hashlib.sha256,"sha1":hashlib.sha1,"md5":hashlib.md5,"sha512":hashlib.sha512,"sha3":hashlib.sha3_256,"blake2b":hashlib.blake2b,"sha384":hashlib.sha384}
n=0
seen=set()
for p in files:
    data=open(p,'rb').read()
    key=sha(data).digest()
    if key in seen: continue
    seen.add(key)
    cands=[("raw",data)] if len(data)<5_000_000 else []
    for an,a in algos.items():
        d=a(data); h=d.hexdigest()
        cands+= [(an+"hex",h.encode()),(an+"HEX",h.upper().encode()),(an+"bin",d.digest()),(an+"hex-sha",sha(h.encode()).hexdigest().encode())]
    for lab,pw in cands:
        n+=1; test(pw,f"{os.path.basename(p)}:{lab}")
print("unique files",len(seen),"tests",n)
