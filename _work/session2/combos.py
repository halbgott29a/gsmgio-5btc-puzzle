import base64, hashlib, itertools, sys, time
from Crypto.Cipher import AES
W=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
BL={"SALPH":load(W+r"\salphaseion_blob.txt"),"COSMIC":load(W+r"\cosmic_blob.txt")}
sha=hashlib.sha256
def kiv(pw,salt):
    a=sha(pw+salt).digest(); b=sha(a+pw+salt).digest(); c=sha(b+pw+salt).digest()
    d=a+b+c; return d[:32],d[32:48]
tails={t:(salt,ct,ct[-32:-16],ct[-16:]) for t,(salt,ct) in BL.items()}
hits=0
def test(pw,label):
    global hits
    for t,(salt,ct,pv,last) in tails.items():
        k,iv=kiv(pw,salt)
        pl=AES.new(k,AES.MODE_CBC,pv).decrypt(last); p=pl[-1]
        if 1<=p<=16 and pl[-p:]==bytes([p])*p:
            full=AES.new(k,AES.MODE_CBC,iv).decrypt(ct); p=full[-1]; body=full[:-p]
            if sum(1 for c in body if 32<=c<127 or c in(9,10,13))/max(1,len(body))>.85:
                print("HIT",t,label,body[:300]); hits+=1
A=["matrixsumlist","lastwordsbeforearchichoice","thispassword","sha256","ourfirsthintisyourlastcommand","enter","anstoo"]
B=A+["yinyang","yellowblueprimes","primes"]
alt={"sha256":["sha256","shabef"],"anstoo":["anstoo","ans","answer"],"ourfirsthintisyourlastcommand":["ourfirsthintisyourlastcommand","fourfirsthintisyourlastcommand"]}
n=0;t0=time.time()
def forms(s):
    b=s.encode(); h=sha(b).hexdigest()
    yield "raw",b; yield "sha",h.encode(); yield "shaU",h.upper().encode(); yield "shabin",sha(b).digest()
    yield "sha2",sha(h.encode()).hexdigest().encode()
def run(pieces,maxk):
    global n
    for k in range(1,maxk+1):
        for perm in itertools.permutations(pieces,k):
            opts=[alt.get(p,[p]) for p in perm]
            for choice in itertools.product(*opts):
                for sep in ("", " "):
                    s=sep.join(choice)
                    for case in (s,s.lower() if sep=="" else s.lower(),s.upper()):
                        for nm,b in forms(case):
                            test(b,f"{nm}:{case[:70]}"); n+=1
                # iterative hash chain (each piece hashed into the next)
                h=b""
                for p in choice:
                    h=sha(h+p.encode()).hexdigest().encode(); 
                test(h,f"chain:{'+'.join(choice)}"); n+=1
                h=b""
                for p in choice:
                    h=sha(p.encode()+h).hexdigest().encode()
                test(h,f"chainR:{'+'.join(choice)}"); n+=1
        print("k",k,"tests",n,round(time.time()-t0),"s",file=sys.stderr)
run(A,7)
print("setA done",n,"hits",hits)
run(B,4)
print("setB done",n,"hits",hits)
