import re,base64,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
from Crypto.Cipher import AES
R=r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle"; F=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
rd=open(R+r"\README.md",encoding='utf8').read()
full=re.search(r'final password as "(causality[^"]+)"',rd).group(1); p3=re.search(r'"(jacquefresco[^"]+)"',rd).group(1)
def evp(pw,salt):
    d=b"";pr=b""
    while len(d)<48: pr=hashlib.sha256(pr+pw+salt).digest(); d+=pr
    return d[:32],d[32:48]
def dec(path,pw):
    b=base64.b64decode("".join(open(path).read().split())); k,iv=evp(pw.encode(),b[8:16])
    pt=AES.new(k,AES.MODE_CBC,iv).decrypt(b[16:]); return pt[:-pt[-1]].decode('utf8','ignore')
T={}
T["phase2"]=dec(R+r"\phase2-assets\phase2_aes.txt",hashlib.sha256(b"causality").hexdigest())
T["phase3"]=dec(R+r"\phase2-assets\phase3_aes.txt",hashlib.sha256(full.encode()).hexdigest())
pk=dec(R+r"\phase3-assets\phase3.2-aes.txt",hashlib.sha256(p3.encode()).hexdigest())
T["phase3.2-pkg"]=re.sub(r'[^\x20-\x7e\r\n]','',pk)
md=open(R+r"\unverified\phase3.2_1141.md",encoding='utf8').read()
T["phase3.2-speech"]=re.search(r"s='(yourlife[a-z']+)'",md).group(1)
import html
p2h=open("ph2/p2.html",encoding='utf8',errors='ignore').read()
T["phase2-page"]=' '.join(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style).*?</\1>','',p2h,flags=re.S|re.I)).split())
cj=open(F+r"\creator_jrk.txt",encoding='utf8',errors='ignore').read()
T["creator-msgs"]=re.sub(r'=== \[[^\]]*\] Jrk Bgrt','',cj)
T["salph-words"]="matrixsumlist enter lastwordsbeforearchichoice thispassword sha256 ourfirsthintisyourlastcommand ans too"
if __name__=="__main__":
    for k,v in T.items():
        l=re.sub(r'[^a-z]','',v.lower())
        print(f"{k:16s} chars={len(v):6d} letters={len(l):6d}",{w:l.count(w) for w in ("salvation","yinyang","yingyang","yin","yang","sal")})
