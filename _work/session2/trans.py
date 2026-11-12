import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, itertools, random, time, multiprocessing as mp
import ckb
dbbi=open(r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work\salph_raw.txt").read().strip()[:91]
def grid(R,C): return [[dbbi[r*C+c] for c in range(C)] for r in range(R)]
def spiral(g,cw=True,start=0):
    R,C=len(g),len(g[0]); out=[]; t,b,l,r=0,R-1,0,C-1
    while t<=b and l<=r:
        for c in range(l,r+1): out.append(g[t][c])
        t+=1
        for rr in range(t,b+1): out.append(g[rr][r])
        r-=1
        if t<=b:
            for c in range(r,l-1,-1): out.append(g[b][c])
            b-=1
        if l<=r:
            for rr in range(b,t-1,-1): out.append(g[rr][l])
            l+=1
    return out
def readings():
    R={}
    for (r,c) in ((7,13),(13,7)):
        g=grid(r,c); T=[list(x) for x in zip(*g)]
        nm=f"{r}x{c}"
        R[nm+"/rows"]=[x for row in g for x in row]
        R[nm+"/cols"]=[x for col in T for x in col]
        R[nm+"/snake-rows"]=[x for i,row in enumerate(g) for x in (row if i%2==0 else row[::-1])]
        R[nm+"/snake-cols"]=[x for i,col in enumerate(T) for x in (col if i%2==0 else col[::-1])]
        R[nm+"/spiral-cw"]=spiral(g)
        R[nm+"/spiral-ccw"]=spiral(T)  # transpose of cw spiral = ccw
        # diagonals
        d=[];  # anti-diagonals
        for s in range(r+c-1):
            for i in range(r):
                j=s-i
                if 0<=j<c: d.append(g[i][j])
        R[nm+"/antidiag"]=d
        d=[]
        for s in range(-(r-1),c):
            for i in range(r):
                j=i+s
                if 0<=j<c: d.append(g[i][j])
        R[nm+"/diag"]=d
    out={}
    for k,v in R.items():
        s="".join(v); assert len(s)==91 and sorted(s)==sorted(dbbi),k
        out[k]=s; out[k+"/rev"]=s[::-1]
    out["identity"]=dbbi
    return out
def job(a):
    name,s,esc,iters,rs,seed=a
    random.seed(seed)
    f,pt=ckb.solve(ckb.tokenize(s,set(esc)),iters,rs)
    return f,name,esc,pt
if __name__=="__main__":
    R=readings(); print(len(R),"readings",file=sys.stderr)
    pairs=list(itertools.combinations("abcdefghi",2))
    jobs=[(n,s,e,3000,4,i) for i,(n,s) in enumerate(R.items()) for e in pairs]
    t0=time.time()
    with mp.Pool(max(1,mp.cpu_count()-1)) as p: res=p.map(job,jobs,chunksize=8)
    res.sort(reverse=True)
    print("screen time",round(time.time()-t0))
    for r in res[:15]: print(f"{r[0]:.3f} {r[1]} esc={r[2]} {r[3][:70]}")
    # refine top 12 with strong solve
    top=res[:12]; jobs2=[(n,R[n],e,8000,10,99+i) for i,(f,n,e,pt) in enumerate(top)]
    with mp.Pool(max(1,mp.cpu_count()-1)) as p: res2=p.map(job,jobs2)
    res2.sort(reverse=True); print("--- refined")
    for r in res2: print(f"{r[0]:.3f} {r[1]} esc={r[2]} {r[3][:70]}")
