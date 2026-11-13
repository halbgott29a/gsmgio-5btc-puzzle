import re,sys
md=open(r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle\unverified\phase3.2_1141.md",encoding='utf8').read()
s=re.search(r"s='(yourlife[a-z']+)'",md).group(1).replace("'","")
def primes(n):
    z=bytearray([1])*(n+1); z[0]=z[1]=0
    for i in range(2,int(n**.5)+1):
        if z[i]: z[i*i::i]=bytearray(len(z[i*i::i]))
    return [i for i in range(n+1) if z[i]]
P=primes(4000)
TARGETS=["salvation","yinyang","yingyang","yin","yang","sal"]
def scan(text,label):
    res=[]
    for rev in (0,1):
        T=text[::-1] if rev else text
        for k in range(len(T)):
            U=T[k:]
            for off in (0,1):               # 0-indexed or 1-indexed
                idx=[p-off for p in P if 0<=p-off<len(U)]
                E="".join(U[i] for i in idx)
                for t in ("salvation","yinyang","yingyang"):
                    for needle in (t,t[::-1]):
                        j=E.find(needle)
                        if j>=0: res.append((label,rev,k,off,needle,E[max(0,j-10):j+len(needle)+10]))
    return res
r=scan(s,"3.2-yourlife")
print("text len",len(s),"hits",len(r))
for x in r[:20]: print(x)
# fixed-length windows of consecutive primes starting at each prime (31 bytes)
