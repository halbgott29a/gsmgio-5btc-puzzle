import base64, hashlib, re
from Crypto.Cipher import AES
R=r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle"
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
def evp(pw,salt,md):
    d=b"";pr=b""
    while len(d)<48: pr=md(pr+pw+salt).digest(); d+=pr
    return d[:32],d[32:48]
def dec(p,pw,md):
    s,c=load(p); k,iv=evp(pw,s,md); pt=AES.new(k,AES.MODE_CBC,iv).decrypt(c); n=pt[-1]
    ok=1<=n<=16 and pt[-n:]==bytes([n])*n
    return ok, pt[:-n][:90] if ok else None
readme=open(R+r"\README.md",encoding="utf8").read()
full=re.search(r'final password as "(causality[^"]+)"',readme).group(1)
p3=re.search(r'"(jacquefresco[^"]+)"',readme).group(1)
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
tests=[("phase2 'causality'",R+r"\phase2-assets\phase2_aes.txt",["causality"]),
 ("phase3 sha256(full pw)",R+r"\phase2-assets\phase3_aes.txt",[sha(full),full]),
 ("phase3.2",R+r"\phase3-assets\phase3.2-aes.txt",[sha(p3),p3])]
for name,f,pws in tests:
    for pw in pws:
        for mn,md in (("sha256",hashlib.sha256),("md5",hashlib.md5)):
            ok,pt=dec(f,pw.encode(),md)
            if ok: print("VALID",name,mn,pw[:30],pt)
    print("done",name)
