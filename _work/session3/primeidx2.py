import re,sys,base64,hashlib
sys.argv=['x']
exec(open('primeidx.py').read().split('r=scan(')[0])
from Crypto.Cipher import AES
R=r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle"
rd=open(R+r"\README.md",encoding='utf8').read()
full=re.search(r'final password as "(causality[^"]+)"',rd).group(1)
p3=re.search(r'"(jacquefresco[^"]+)"',rd).group(1)
def evp(pw,salt):
    d=b"";pr=b""
    while len(d)<48: pr=hashlib.sha256(pr+pw+salt).digest(); d+=pr
    return d[:32],d[32:48]
def dec(path,pw):
    b=base64.b64decode("".join(open(path).read().split())); k,iv=evp(pw.encode(),b[8:16])
    pt=AES.new(k,AES.MODE_CBC,iv).decrypt(b[16:]); return pt[:-pt[-1]].decode('utf8','ignore')
phase3=dec(R+r"\phase2-assets\phase3_aes.txt",hashlib.sha256(full.encode()).hexdigest())
p32=open('p32.txt','rb').read().decode('utf8','ignore')
texts={"phase3-plaintext":phase3,"phase3.2-package":p32,"phase3-password":full,"phase3.2-password":p3}
for k,v in list(texts.items()): print(k,len(v))
for name,t in texts.items():
    L=re.sub(r'[^a-z]','',t.lower())
    r=scan(L,name); print(name,"letters",len(L),"hits",len(r)); [print("  ",x) for x in r[:5]]
