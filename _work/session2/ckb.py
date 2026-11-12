import re, math, collections, random, itertools, sys, glob, time
random.seed(7)
txt="".join(open(f,encoding='utf8',errors='ignore').read() for f in glob.glob("corpus/pg*.txt"))
txt=re.sub(r'[^A-Za-z]','',txt).upper().replace('J','I')   # 25-letter alphabet (I/J merged)
N=len(txt); print("corpus letters",N,file=sys.stderr)
quad=collections.Counter(txt[i:i+4] for i in range(N-3))
tot=N-3; floor=math.log10(0.1/tot)
Q={k:math.log10(v/tot) for k,v in quad.items()}
def fit(s):  # mean log10 per quadgram
    if len(s)<4: return -9
    return sum(Q.get(s[i:i+4],floor) for i in range(len(s)-3))/(len(s)-3)
L25="ABCDEFGHIKLMNOPQRSTUVWXYZ"
def tokenize(sym,esc):
    toks=[];i=0
    while i<len(sym):
        if sym[i] in esc:
            if i+1>=len(sym): break
            toks.append(sym[i:i+2]); i+=2
        else: toks.append(sym[i]); i+=1
    return toks
def solve(toks,iters=6000,restarts=10):
    import math
    types=sorted(set(toks)); T=len(types)
    idx={t:i for i,t in enumerate(types)}; seq=[idx[t] for t in toks]
    best=(-99,None)
    for _ in range(restarts):
        letters=random.sample(L25,len(L25)); key=letters[:T]; unused=letters[T:]
        def ev(k): return fit("".join(k[i] for i in seq))
        cur=ev(key); bk=(cur,key[:])
        for it in range(iters):
            temp=0.12*(1-it/iters)+1e-4
            k2=key[:]; j=None
            if unused and random.random()<.3:
                a=random.randrange(T); j=random.randrange(len(unused)); k2[a],u=unused[j],k2[a]
            else:
                a,b=random.sample(range(T),2); k2[a],k2[b]=k2[b],k2[a]
            f=ev(k2)
            if f>cur or random.random()<math.exp((f-cur)/temp):
                if j is not None: unused[j]=u
                key,cur=k2,f
                if cur>bk[0]: bk=(cur,key[:])
        if bk[0]>best[0]: best=(bk[0],"".join(bk[1][i] for i in seq))
    return best
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="calib":
        # real English message, encode with random 9-symbol, 2-escape checkerboard, then solve
        msg=("THEPRIVATEKEYISHIDDENINSIDETHEMATRIXANDONLYTHOSEWHOSEEKTHETRUTHWILLFINDITBEHINDTHEDOOR")
        msg=msg.replace('J','I')[:60]
        for trial in range(4):
            esc=random.sample("abcdefghi",2); singles=[c for c in "abcdefghi" if c not in esc]
            cells=[(s,) for s in singles]+[(e,x) for e in sorted(esc) for x in "abcdefghi"]
            letters=random.sample(L25,25); board={l:"".join(c) for l,c in zip(letters,cells)}
            ct="".join(board[ch] for ch in msg)
            toks=tokenize(ct,set(esc)); f,pt=solve(toks)
            print(f"esc={esc} ct_len={len(ct)} toks={len(toks)} fit={f:.3f} true_fit={fit(msg):.3f} recovered={pt==msg}  {pt[:40]}")
    else:
        dbbi=open(r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work\salph_raw.txt").read().strip()[:91]
        res=[]
        t0=time.time()
        for esc in itertools.combinations("abcdefghi",2):
            toks=tokenize(dbbi,set(esc)); f,pt=solve(toks,6000,6); res.append((f,esc,len(toks),pt))
        res.sort(reverse=True)
        for r in res[:8]: print(f"{r[0]:.3f} esc={r[1]} toks={r[2]} {r[3]}")
        print("time",round(time.time()-t0))
        # null: shuffled dbbi, best over all pairs
        for s in range(3):
            l=list(dbbi); random.shuffle(l); l="".join(l); best=-9
            for esc in itertools.combinations("abcdefghi",2):
                f,_=solve(tokenize(l,set(esc)),6000,6); best=max(best,f)
            print("null shuffle best over pairs:",round(best,3))
