#!/usr/bin/env python3
"""Hill-climb the straddling-checkerboard ALPHABET for dbbi, with escape digits
fixed (b,e -> 1,4 in a0i8, the 3.2.2 convention; also try 2,5). Trigram fitness
trained on real English text from the repo. Tests if dbbi is a plain checkerboard."""
import random, re, math, collections, os
random.seed(0)

# ---- train trigram model on English text we have ----
corpus=""
for p in [r"D:\tmp\gsmgio-5btc-puzzle\README.md", r"D:\tmp\gsmgio-5btc-puzzle\_work\cosmicduality.txt"]:
    if os.path.exists(p): corpus+=open(p,encoding="utf-8",errors="replace").read()
corpus=re.sub(r'[^A-Za-z]','',corpus).upper()
tri=collections.Counter(corpus[i:i+3] for i in range(len(corpus)-2))
total=sum(tri.values()); floor=math.log(0.01/total)
def fitness(s):
    s=re.sub(r'[^A-Z]','',s.upper())
    if len(s)<3: return -1e9
    return sum(math.log(tri[s[i:i+3]]/total) if s[i:i+3] in tri else floor for i in range(len(s)-2))/(len(s)-2)

dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"

def decode(digits, alpha28, e1, e2):
    e1,e2=sorted((e1,e2))
    top=[c for c in range(10) if c not in (e1,e2)]
    bd={}
    for k,c in enumerate(top): bd[str(c)]=alpha28[k]
    for c in range(10): bd[f"{e1}{c}"]=alpha28[8+c]
    for c in range(10): bd[f"{e2}{c}"]=alpha28[18+c]
    out=[];i=0
    while i<len(digits):
        d=int(digits[i])
        if d in (e1,e2):
            if i+1>=len(digits): break
            out.append(bd.get(digits[i:i+2],'?'));i+=2
        else: out.append(bd.get(digits[i],'?'));i+=1
    return "".join(out)

LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZ.."   # 28 cells (26 letters + 2 fillers)

def hillclimb(digits,e1,e2,iters=20000):
    best=list(LETTERS); random.shuffle(best)
    bf=fitness(decode(digits,"".join(best),e1,e2))
    for _ in range(iters):
        a,b=random.sample(range(28),2)
        cand=best[:]; cand[a],cand[b]=cand[b],cand[a]
        f=fitness(decode(digits,"".join(cand),e1,e2))
        if f>bf: best,bf=cand,f
    return bf,"".join(best),decode(digits,"".join(best),e1,e2)

configs=[("a0i8",{c:str(i) for i,c in enumerate("abcdefghi")},1,4),
         ("a1i9",{c:str(i+1) for i,c in enumerate("abcdefghi")},2,5),
         ("a0i8",{c:str(i) for i,c in enumerate("abcdefghi")},2,5)]
# baseline: fitness of real english for reference
print("ref fitness (real English sample):",round(fitness("INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEY"),3))
print("ref fitness (random letters):",round(fitness("XQZJVKWBFPMGYTRNDLAOSCEUIH"),3))
for name,mp,e1,e2 in configs:
    dig="".join(mp[c] for c in dbbi)
    results=[hillclimb(dig,e1,e2) for _ in range(6)]   # 6 restarts
    bf,key,txt=max(results,key=lambda x:x[0])
    print(f"\n[{name} esc{e1}{e2}] best fitness={bf:.3f}")
    print(f"   key={key}")
    print(f"   decode={txt}")
