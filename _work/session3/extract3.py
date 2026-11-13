import sys,re,time,collections
sys.path.insert(0,'.')
src=open('extract.py').read().split("t0=time.time()")[0]
exec(src)
from imgderived import SER
SEQ.clear()
for name,v in SER.items():
    v=[x for x in v if x>=0]
    if not v: continue
    SEQ[name]=v
    SEQ[name+"|+1"]=[x+1 for x in v]
    SEQ[name+"|sorted"]=sorted(set(v))
    if all(x>0 for x in v):
        # cumulative skip pattern, repeated cyclically
        pos=[];c=0
        for i in range(4000):
            c+=v[i%len(v)]
            if c>6000: break
            pos.append(c)
        SEQ[name+"|cumcyc"]=pos
        SEQ[name+"|cumonce"]=list(itertools.accumulate(v))
SEQ["allcolored_byte#"]=sorted(SER["yellow_byte#"]+SER["blue_byte#"])
print("series",len(SEQ),file=sys.stderr)
t0=time.time()
for name,text in T.items():
    words_mode(name,text); letters_mode(name,text); print(name,ntests,round(time.time()-t0),"s",file=sys.stderr)
def src_has(label,needle):
    nm=label.split('|')[0]; L=re.sub(r'[^a-z]','',T[nm].lower()); return needle in L or needle[::-1] in L
gen=[h for h in hits if not src_has(h[0],h[1])]
print("tests",ntests,"raw",len(hits),"trivial",len(hits)-len(gen),"GENUINE",len(gen))
print(collections.Counter((h[0].split('|')[0],h[1]) for h in gen))
for h in [x for x in gen if not x[0].startswith('creator')][:15]: print(h)
