import sys,itertools,re,time,hashlib
sys.path.insert(0,'.')
src=open('matsum.py').read().split("classes=['k'")[0]
exec(src)                      # gives nb (trusted grid with 'f' cell), dbbi, D
src2=open('imgpw.py').read().split("def fmts(v)")[0]
exec(src2)                     # test(), sha, BL, hits ... (imports imgderived too)
def fmts(v):
    v=list(v)
    out={"".join(map(str,v)),",".join(map(str,v)),", ".join(map(str,v))," ".join(map(str,v)),"".join(f"{x:02x}" for x in v),
         "".join(chr(96+((x-1)%26+1)) for x in v),str(sum(v))}
    return {o for o in out if o}
from corpus_texts import T as TXT
LET={k:re.sub(r'[^a-z]','',t.lower()) for k,t in TXT.items()}
def idx_search(v,label):
    for nm,L in LET.items():
        for rev in (0,1):
            S=L[::-1] if rev else L
            for off in (0,1):
                for seq in (v,list(itertools.accumulate(v)),[x+1 for x in v]):
                    E="".join(S[x-off] for x in seq if 0<=x-off<len(S))
                    for t in ("salvation","yinyang","yingyang"):
                        if t in E or t[::-1] in E:
                            if t not in L and t[::-1] not in L: print("IDXHIT",label,nm,rev,off,t,E[:60])
words=["matrixsumlist","enter","lastwordsbeforearchichoice","thispassword","sha256","ans","yellow","blue","primes","red","white"]
seen=set(); n=0; t0=time.time(); lists=0
for perm in itertools.permutations((2,3,5,7)):
    cv=dict(zip(('w','r','b','y'),perm))
    for black in (0,1):
        for fe in ('white','zero','eleven'):
            for redrow in ('none','top','bottom'):
                val={'k':black,'w':cv['w'],'b':cv['b'],'y':cv['y'],'f':{'white':cv['w'],'zero':0,'eleven':11}[fe]}
                M=[[val[x] for x in row] for row in nb]
                if redrow=='top': M=[[cv['r']]*14]+M
                if redrow=='bottom': M=M+[[cv['r']]*14]
                R=[sum(r) for r in M]; C=[sum(M[i][j] for i in range(len(M))) for j in range(14)]
                for lst in (R,C,R+C,C+R,[sum(R)]):
                    key=tuple(lst)
                    if key in seen: continue
                    seen.add(key); lists+=1
                    idx_search(lst,f"{perm}|k{black}|fe-{fe}|red-{redrow}")
                    for s in fmts(lst):
                        run=lambda x,l:(test(x.encode(),l),test(sha(x.encode()).hexdigest().encode(),l+"|sha"))
                        run(s,s[:30]); n+=2
                        for w in words:
                            run(w+s,w+"+"+s[:20]); run(s+w,s[:20]+"+"+w); n+=4
print("distinct sum-lists",lists,"AES tests",n,"hits",hits,round(time.time()-t0),"s")
