import sys
sys.argv=['x']
src=open('prime_zero.py').read().split("bases={")[0]
exec(src)
# sanity: recover known segment
s1=tail.split('z')[1]
tr=str.maketrans('abcdefghio','1234567890')
reports.clear(); from_digits(s1.translate(tr),"SANITY-s1")
print("sanity:",reports)
import itertools
tests=0
for bn,s in {"dbbi":dbbi,"faed":faed,"dbbi+faed":dbbi+faed,"raw":raw[:765],"faed+dbbi":faed+dbbi}.items():
    for mn,off in (("a1",1),("a0",0)):
        vals=[ "abcdefghi".index(c)+off if c in "abcdefghi" else None for c in s]
        for r in range(1,5):
            for sub in itertools.combinations([2,3,5,7],r):
                S=set(sub)
                for comp in (False,True):  # act on values in S, or on values not in S
                    hit=[(v is not None and ((v in S)!=comp)) for v in vals]
                    A="".join("0" if h else str(v) for h,v in zip(hit,vals))
                    B="".join(str(v) for h,v in zip(hit,vals) if not h)
                    C="".join(str(v) for h,v in zip(hit,vals) if h)
                    for v_,ds in (("zero",A),("del",B),("keep",C)):
                        tests+=1; from_digits(ds,f"{bn}/{mn}/{sub}/{'not' if comp else 'in'}/{v_}")
                        from_digits(ds[::-1],f"{bn}/{mn}/{sub}/{'not' if comp else 'in'}/{v_}/rev")
print("tests",tests)
for r in reports: print(r)
