#!/usr/bin/env python3
"""Combined VIC decode on dbbi: columnar transposition + mod-9 over-encryption
('matrixsumlist') + straddling checkerboard. Strict anti-apophenia scoring."""
import itertools
from cb2 import decode, pad, kw   # reuse validated decoder

dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"

def seqkey(word):
    word=word.upper()
    order=sorted(range(len(word)),key=lambda i:(word[i],i))
    rank=[0]*len(word)
    for r,i in enumerate(order): rank[i]=r+1
    return rank   # 1..len

def key_order(key):
    return [i for i,_ in sorted(enumerate(key),key=lambda x:(x[1],x[0]))]
def col_decrypt(cipher,key):
    w=len(key);n=len(cipher);order=key_order(key);nrows=-(-n//w)
    rem=n%w
    col_len={c:(nrows if (rem==0 or c<rem) else nrows-1) for c in range(w)}
    cols={};pos=0
    for c in order:
        cols[c]=cipher[pos:pos+col_len[c]];pos+=col_len[c]
    out=[]
    for r in range(nrows):
        for c in range(w):
            if r<len(cols[c]): out.append(cols[c][r])
    return "".join(out)
def col_encrypt(text,key):
    w=len(key);order=key_order(key)
    rows=[text[i:i+w] for i in range(0,len(text),w)]
    return "".join(r[c] for c in order for r in rows if c<len(r))

WORDS=set("THE AND THAT HAVE FOR NOT WITH YOU THIS BUT FROM THEY KEY PRIVATE PASSWORD MATRIX PRIME ENTER DOOR HALF BETTER YELLOW BLUE CRACK BITCOIN GIVE AWAY FRONT EYES LAST STEP TRUE GSMG BELONG FUNDS LIVE NEED ALSO YOUR WORD PASS CODE SOURCE WALLET ADDRESS SECRET MESSAGE FOLLOW WHITE RABBIT HERE OPEN LOCK ARE NOW ONE TWO SUM LIST BEFORE CHOICE YANG YIN ANSWER ROOM NEO ARCHITECT YOUVE EARNED TAKE WISEMAN HUNDRED INVESTMENT".split())
W=set(w for w in WORDS if len(w)>=3)
LONGW=set(w for w in WORDS if len(w)>=4)
def eng(s):
    s=s.upper().replace('.','').replace('?','')
    sc=sum(len(w)*s.count(w) for w in W)
    longhits=sum(1 for w in LONGW if w in s)
    return sc, longhits

alphabets={"3.2.2":"FUBCDORA.LETHINGKYMVPS.JQZXW","matrixsumlist":kw("MATRIXSUMLIST"),
 "enter":kw("ENTER"),"plain":kw(""),"yellowblue":kw("YELLOWBLUE")}
maps={"a1i9":{c:i+1 for i,c in enumerate("abcdefghi")},
      "a0i8":{c:i for i,c in enumerate("abcdefghi")}}

# over-encryption key streams (subtract mod 9/10)
oversrc={"none":None,"msl_seq":seqkey("MATRIXSUMLIST"),"msl_digits":[ (ord(c)-96) for c in "matrixsumlist"]}

best=[]
transforms={"none":lambda s:s,
            "coldec_msl":lambda s:col_decrypt(s,"matrixsumlist"),
            "colenc_msl":lambda s:col_encrypt(s,"matrixsumlist"),
            "rev":lambda s:s[::-1]}
for tn,tf in transforms.items():
    d2=tf(dbbi)
    for mn,mp in maps.items():
        digs=[mp[c] for c in d2]
        for on,ov in oversrc.items():
            for mod in (9,10):
                if ov is None:
                    dd="".join(str(x) for x in digs)
                else:
                    dd="".join(str((digs[i]-ov[i%len(ov)])%mod) for i in range(len(digs)))
                for an,al in alphabets.items():
                    if len(al)!=28: continue
                    for e1,e2 in itertools.combinations(range(10),2):
                        s=decode(dd,al,e1,e2)
                        sc,lh=eng(s)
                        if lh>=3 or sc>=14:
                            best.append((lh,sc,f"{tn}/{mn}/{on}/m{mod}/{an}/e{e1}{e2}",s))
best.sort(reverse=True)
print(f"combined VIC sweep: hits (>=3 long words or score>=14): {len(best)}")
for lh,sc,l,s in best[:20]:
    print(f"[long{lh} sc{sc}] {l:34} {s[:62]}")
if not best: print("NOTHING above anti-apophenia threshold.")
