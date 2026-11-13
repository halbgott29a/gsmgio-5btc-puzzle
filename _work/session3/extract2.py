import re,sys,math,time,itertools
sys.path.insert(0,'.')
from corpus_texts import T
def sieve(n):
    z=bytearray([1])*(n+1); z[0]=z[1]=0
    for i in range(2,int(n**.5)+1):
        if z[i]: z[i*i::i]=bytearray(len(z[i*i::i]))
    return z
N=30000; Z=sieve(N)
P=[i for i in range(N+1) if Z[i]]
SEQ={
 "prime":P,"prime+1":[p+1 for p in P],"prime-1":[p-1 for p in P],"prime^2":[p*p for p in P if p*p<N],
 "oddprime":P[1:],"nonprime(composite)":[i for i in range(4,3000) if not Z[i]],"nonprime+1":[i for i in range(1,3000) if not Z[i]],
 "square":[i*i for i in range(1,170)],"triangular":[i*(i+1)//2 for i in range(1,240)],"cube":[i**3 for i in range(1,40)],
 "fibonacci":[a for a,b in [(1,2)] for _ in [0]] ,"pow2":[2**i for i in range(0,14)],"twinprime":[p for p in P if p+2<N and Z[p+2]],
 "semiprime":[n for n in range(4,3000) if sum(1 for p in P if p*p<=n and n%p==0)>=1 and (lambda q:(q>1 and Z[q]))(n//next(p for p in P if n%p==0))],
 "evens":list(range(0,3000,2)),"odds":list(range(1,3000,2)),"prime-index-of-prime":[P[p-1] for p in P if p-1<len(P) and P[p-1]<N],
}
fib=[1,2]
while fib[-1]<N: fib.append(fib[-1]+fib[-2])
SEQ["fibonacci"]=fib
TARG=("salvation","yinyang","yingyang")
hits=[]; ntests=0
def check(E,label):
    global ntests
    ntests+=1
    for t in TARG:
        for needle in (t,t[::-1]):
            j=E.find(needle)
            if j>=0: hits.append((label,needle,E[max(0,j-12):j+len(needle)+12]))
def letters_mode(name,text):
    L=re.sub(r'[^a-z]','',text.lower())
    starts=[0]+[m.start() for m in re.finditer(r'(?<![a-z])[a-z]',text.lower())]   # word starts (index in text, convert to letter index)
    # map word starts to letter indices
    li=[];cnt=0
    for ch in text.lower():
        pass
    idx=[];c=0
    prev=False
    for ch in text.lower():
        if 'a'<=ch<='z':
            if not prev: idx.append(c)
            c+=1; prev=True
        else: prev=False
    idx=sorted(set([0]+idx))
    if len(idx)>1500: idx=idx[::max(1,len(idx)//1500)]
    for rev in (0,1):
        S=L[::-1] if rev else L
        for k in idx:
            U=S[k:]; n=len(U)
            for sn,seq in SEQ.items():
                for off in (0,1):
                    E="".join(U[s-off] for s in seq if 0<=s-off<n)
                    check(E,f"{name}|letters|rev{rev}|start{k}|{sn}|off{off}")
def words_mode(name,text):
    W=re.findall(r"[A-Za-z']+",text)
    def lastwords(sep):
        parts=[p for p in re.split(sep,text) if re.search(r'[A-Za-z]',p)]
        return [re.findall(r"[A-Za-z']+",p)[-1] for p in parts]
    LISTS={"allwords":W,"lastword/sentence":lastwords(r'[.!?]+'),"lastword/line":lastwords(r'[\r\n]+'),"lastword/para":lastwords(r'(?:\r?\n){2,}')}
    for ln,Wl in LISTS.items():
        for rev in (0,1):
            X=Wl[::-1] if rev else Wl; n=len(X)
            for sn,seq in SEQ.items():
                for off in (0,1):
                    sel=[X[s-off] for s in seq if 0<=s-off<n]
                    if not sel: continue
                    for um,fn in (("whole",lambda w:w),("first",lambda w:w[0]),("last",lambda w:w[-1]),("second",lambda w:w[1] if len(w)>1 else ''),("penult",lambda w:w[-2] if len(w)>1 else '')):
                        E="".join(fn(w) for w in sel).lower(); E=re.sub(r'[^a-z]','',E)
                        check(E,f"{name}|{ln}|rev{rev}|{sn}|off{off}|{um}")
t0=time.time()
for name,text in T.items():
    words_mode(name,text); print(name,"words done",ntests,round(time.time()-t0),"s",file=sys.stderr)
    letters_mode(name,text); print(name,"letters done",ntests,round(time.time()-t0),"s",file=sys.stderr)

import collections
def src_has(label,needle):
    name=label.split('|')[0]; L=re.sub(r'[^a-z]','',T[name].lower()); return needle in L or needle[::-1] in L
genuine=[h for h in hits if not src_has(h[0],h[1])]
print("tests",ntests,"raw hits",len(hits),"| trivial (word already in source)",len(hits)-len(genuine),"| GENUINE",len(genuine))
c=collections.Counter((h[0].split('|')[0],h[1]) for h in genuine); print(c)
for h in genuine[:20]: print(h)
