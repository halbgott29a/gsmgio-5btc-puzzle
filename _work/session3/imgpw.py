import sys,hashlib,base64,itertools,time
sys.path.insert(0,'.')
from imgderived import SER
from Crypto.Cipher import AES
W=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
BL={"SALPH":load(W+r"\salphaseion_blob.txt"),"COSMIC":load(W+r"\cosmic_blob.txt")}
sha=hashlib.sha256
T={t:(s,ct,ct[-32:-16],ct[-16:]) for t,(s,ct) in BL.items()}
def kiv(pw,salt,md):
    d=b"";pr=b""
    while len(d)<48: pr=md(pr+pw+salt).digest(); d+=pr
    return d[:32],d[32:48]
hits=0
def test(pw,label):
    global hits
    for md in (hashlib.sha256,hashlib.md5):
        for t,(salt,ct,pv,last) in T.items():
            k,iv=kiv(pw,salt,md); pl=AES.new(k,AES.MODE_CBC,pv).decrypt(last); p=pl[-1]
            if 1<=p<=16 and pl[-p:]==bytes([p])*p:
                full=AES.new(k,AES.MODE_CBC,iv).decrypt(ct); p=full[-1]; body=full[:-p]
                if sum(1 for c in body if 32<=c<127 or c in(9,10,13))/max(1,len(body))>.85:
                    print("HIT",t,md.__name__,label,body[:300]); hits+=1
def fmts(v):
    out={"".join(map(str,v)),",".join(map(str,v)),", ".join(map(str,v))," ".join(map(str,v)),"".join(f"{x:02x}" for x in v),
         "".join(chr(96+((x-1)%26+1)) for x in v),"".join(chr(64+((x-1)%26+1)) for x in v),"".join(chr(x) for x in v if 32<=x<127),
         str(sum(v)),"".join(map(str,sorted(v))),"".join(map(str,v[::-1]))}
    return {o for o in out if o}
nums=set()
for k,v in SER.items():
    nums|=fmts(v)
for a,b in (("yellow_byte#","blue_byte#"),("yellow_prime_byte#","blue_prime_byte#"),("yellow_spiral_idx","blue_spiral_idx"),("yellow_spiral_idx_prime","blue_spiral_idx_prime"),("rowsum_bits","colsum_bits"),("rowsum_black","colsum_black")):
    nums|=fmts(SER[a]+SER[b]); nums|=fmts(SER[b]+SER[a])
words=["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword","sha256","ourfirsthintisyourlastcommand","ans","anstoo","yellow","blue","primes","yellowblueprimes","yinyang","11110"]
pieces=sorted(nums)+words
print("number strings",len(nums),"pieces",len(pieces),file=sys.stderr)
n=0;t0=time.time()
def run(s,label):
    global n
    b=s.encode(); test(b,label); test(sha(b).hexdigest().encode(),label+"|sha"); n+=2
for p in pieces: run(p,p[:40])
for a in pieces:
    for b in pieces:
        if a==b: continue
        for sep in ("", " "):
            run(a+sep+b,(a[:20]+"+"+b[:20]))
print("tests(x kdf x blobs)",n,"hits",hits,round(time.time()-t0),"s")
# --- direct readings: do any series read as words?
print("--- readable conversions (letters only, >=5 long):")
for k,v in SER.items():
    for nm,fn in (("a=1 mod26",lambda x:chr(96+((x-1)%26+1))),("chr(x+64)",lambda x:chr(x+64) if 65<=x+64<=90 else '.'),("chr(x+96)",lambda x:chr(x+96) if 97<=x+96<=122 else '.'),("chr(x)",lambda x:chr(x) if 32<=x<127 else '.')):
        s="".join(fn(x) for x in v)
        if len(v)>=5 and sum(c.isalpha() for c in s)>=len(s)*.9 and nm!="a=1 mod26": print(f"  {k:26s}{nm:10s}{s}")
