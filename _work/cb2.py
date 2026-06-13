#!/usr/bin/env python3
"""Correct straddling-checkerboard (dcode VIC layout), validated on phase 3.2.2,
then swept against dbbi."""
import itertools, re

def build(alphabet28, e1, e2):
    e1,e2=sorted((e1,e2))
    top_cols=[c for c in range(10) if c not in (e1,e2)]
    bd={}
    for k,c in enumerate(top_cols): bd[str(c)]=alphabet28[k]
    for c in range(10): bd[f"{e1}{c}"]=alphabet28[8+c]
    for c in range(10): bd[f"{e2}{c}"]=alphabet28[18+c]
    return bd,e1,e2

def decode(digits, alphabet28, e1, e2):
    bd,e1,e2=build(alphabet28,e1,e2)
    out=[];i=0
    while i<len(digits):
        d=int(digits[i])
        if d in (e1,e2):
            if i+1>=len(digits): break
            out.append(bd.get(digits[i:i+2],'?')); i+=2
        else:
            out.append(bd.get(digits[i],'?')); i+=1
    return "".join(out)

# ---- VALIDATE ----
num="15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
A="FUBCDORA.LETHINGKYMVPS.JQZXW"
val=decode(num,A,1,4)
print("VALIDATION 3.2.2:",val)
assert val.replace('.','').startswith("INCASEYOUMANAGE"), "decoder wrong!"
print("decoder OK\n")

# ---- dbbi sweep ----
dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
# a-i -> digits. dbbi has no 'o', so only 1-9 (or 0-8)
maps={"a1i9":{c:str(i+1) for i,c in enumerate("abcdefghi")},
      "a0i8":{c:str(i) for i,c in enumerate("abcdefghi")}}
WORDS=set("THE AND THAT HAVE FOR NOT WITH YOU THIS BUT HIS FROM THEY KEY PRIVATE PASSWORD MATRIX PRIME ENTER DOOR HALF BETTER YELLOW BLUE CRACK BITCOIN GIVE AWAY FRONT EYES LAST STEP TRUE GSMG BELONG FUNDS LIVE NEED ALSO YOUR WORD PASS CODE SOURCE WALLET ADDRESS SECRET MESSAGE FOLLOW WHITE RABBIT HOLE DOWN HERE OPEN LOCK ARE NOW ONE TWO SUM LIST WORDS BEFORE CHOICE YANG YIN ANSWER ROOM NEO".split())
W=set(w for w in WORDS if len(w)>=3)
def eng(s):
    s=s.upper().replace('.','').replace('?','')
    return sum(len(w)*s.count(w) for w in W)

# candidate alphabets (28 syms; pad with . to 28)
def pad(s):
    s="".join(dict.fromkeys(s))  # dedupe keep order
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if ch not in s: s+=ch
    s=s[:26]
    return s[:8]+"."+s[8:17]+"."+s[17:26]  # 8 +1+9 +1+9 = 28
def kw(key):  # keyword-led alphabet
    return pad(key.upper())
alphabets={
 "3.2.2":"FUBCDORA.LETHINGKYMVPS.JQZXW",
 "matrixsumlist":kw("MATRIXSUMLIST"),
 "enter":kw("ENTER"),
 "plain":kw(""),
 "yellowblue":kw("YELLOWBLUE"),
 "salphaseion":kw("SALPHASEION"),
 "thematrixhasyou":kw("THEMATRIXHASYOU"),
}

best=[]
for mn,mp in maps.items():
    digits="".join(mp[c] for c in dbbi)
    for an,al in alphabets.items():
        if len(al)!=28: continue
        for e1,e2 in itertools.combinations(range(10),2):
            s=decode(digits,al,e1,e2)
            sc=eng(s)
            if sc>=10:
                best.append((sc,f"{mn}/{an}/esc{e1}{e2}",s))
best.sort(reverse=True)
print(f"dbbi sweep: candidates score>=10: {len(best)}")
for sc,l,s in best[:15]:
    print(f"[{sc:3d}] {l:28} {s}")
if not best:
    print("none >=10. Top regardless:")
    allr=[]
    for mn,mp in maps.items():
        digits="".join(mp[c] for c in dbbi)
        for an,al in alphabets.items():
            if len(al)!=28: continue
            for e1,e2 in itertools.combinations(range(10),2):
                s=decode(digits,al,e1,e2); allr.append((eng(s),f"{mn}/{an}/esc{e1}{e2}",s))
    allr.sort(reverse=True)
    for sc,l,s in allr[:10]: print(f"[{sc:3d}] {l:28} {s}")
