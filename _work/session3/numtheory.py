import math, random, itertools
raw=open(r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work\salph_raw.txt").read().strip()
dbbi=raw[:91]; blob=raw[91:195]; faed=raw[195:765]
A="abcdefghi"
def num(s,base,off): 
    n=0
    for c in s: n=n*base+A.index(c)+off
    return n
def is_prime(n,k=24):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for _ in range(k):
        a=random.randrange(2,n-1); x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def sieve(N):
    s=bytearray([1])*(N+1); s[0]=s[1]=0
    for i in range(2,int(N**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(N+1) if s[i]]
PR=sieve(3_000_000)
def small_factors(n):
    f=[]
    for p in PR:
        if p*p>n: break
        while n%p==0: f.append(p); n//=p
    return f,n
readings={}
for nm,s in (("dbbi",dbbi),("faed",faed),("dbbi+faed",dbbi+faed),("faed+dbbi",faed+dbbi)):
    for base,off,lab in ((10,1,"dec a=1"),(9,0,"b9 a=0"),(10,0,"dec a=0"),(9,1,"b9 a=1(overflow)")):
        if base==9 and off==1: continue
        for rev in (0,1):
            ss=s[::-1] if rev else s
            readings[f"{nm}|{lab}|{'rev' if rev else 'fwd'}"]=num(ss,base,off)
print("readings",len(readings))
for k,n in readings.items():
    pr=is_prime(n)
    # also n+-1 prime
    pm=[d for d in (-2,-1,1,2) if is_prime(n+d)]
    f,rest=small_factors(n)
    flag="  <<< PRIME" if pr else ""
    print(f"{k:32s} bits={n.bit_length():5d} prime={pr}{flag} near-prime(n+d)={pm} smallfactors(<3e6)={f[:12]}{'...' if len(f)>12 else ''} cofactor_bits={rest.bit_length()}")
# relations between dbbi and faed numbers
for lab in ("dec a=1","b9 a=0","dec a=0"):
    for r in ("fwd","rev"):
        D=readings[f"dbbi|{lab}|{r}"]; F=readings[f"faed|{lab}|{r}"]
        g=math.gcd(D,F)
        print(f"gcd(dbbi,faed) {lab} {r}: {g if g<10**30 else '(big)'}   faed mod dbbi={F%D if D else 0}")
# perfect powers
def iroot(n,k):
    lo,hi=0,1<<(n.bit_length()//k+1)
    while lo<hi:
        mid=(lo+hi+1)//2
        if mid**k<=n: lo=mid
        else: hi=mid-1
    return lo
for k,n in readings.items():
    for e in (2,3,5,7):
        r=iroot(n,e)
        if r**e==n: print("PERFECT POWER",k,e)
