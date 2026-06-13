#!/usr/bin/env python3
"""Columnar transposition hypothesis (from chat line 31761):
key 'matrixsumlist' (len13) keys dbbi (91=7x13); key
'lastwordsbeforearchichoicethispassword' (len38) keys faed (570=15x38).
Try encrypt & decrypt both orientations, then decode a-i->digits->ASCII."""
import re
dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"
faed="faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahigceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgdeefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgiecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchcbafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeggdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiifdgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbeiichiedifbehgbccahhbiibibbibdcbahaidhfahiihic"

def key_order(key):
    # column read order: sort by (letter, original_index)
    return [i for i,_ in sorted(enumerate(key), key=lambda x:(x[1],x[0]))]

def col_encrypt(text, key):
    w=len(key); order=key_order(key)
    rows=[text[i:i+w] for i in range(0,len(text),w)]
    out=[]
    for col in order:
        for r in rows:
            if col<len(r): out.append(r[col])
    return "".join(out)

def col_decrypt(cipher, key):
    w=len(key); n=len(cipher); order=key_order(key)
    nrows=-(-n//w)
    # column lengths (last row may be short)
    full_cols=n-(w*(nrows-1)) if n%w else w
    col_len={c:(nrows if (c< (n% w if n%w else w)) else nrows-1) for c in range(w)} if n%w else {c:nrows for c in range(w)}
    # assign cipher slices to columns in key order
    cols={}; pos=0
    for c in order:
        L=col_len[c]; cols[c]=cipher[pos:pos+L]; pos+=L
    # read row-wise
    out=[]
    for r in range(nrows):
        for c in range(w):
            if r<len(cols[c]): out.append(cols[c][r])
    return "".join(out)

def a2n(s):
    m={c:str(i+1) for i,c in enumerate("abcdefghi")}; m['o']='0'
    return "".join(m.get(c,'?') for c in s)
def ascii_dec(s):
    d=a2n(s)
    for bs in (2,3):
        out="".join(chr(int(d[i:i+bs])) if 32<=int(d[i:i+bs])<=126 else '.' for i in range(0,len(d)-bs+1,bs))
        ok=sum(c!='.' for c in out)/max(1,len(out))
        yield bs,ok,out
def show(label,s):
    print(f"\n[{label}] {s[:80]}")
    for bs,ok,out in ascii_dec(s):
        if ok>0.6: print(f"     a{bs} ascii (ok={ok:.2f}): {out[:70]}")

KEY1="matrixsumlist"
KEY2="lastwordsbeforearchichoicethispassword"
print("KEY1 len",len(KEY1),"dbbi",len(dbbi),"=>",len(dbbi)/len(KEY1),"rows")
print("KEY2 len",len(KEY2),"faed",len(faed),"=>",len(faed)/len(KEY2),"rows")
print("key_order(matrixsumlist):",key_order(KEY1))

for label,fn in (("dbbi col_decrypt",col_decrypt),("dbbi col_encrypt",col_encrypt)):
    show(label, fn(dbbi,KEY1))
    show(label+" REVkey", fn(dbbi,KEY1[::-1]))
for label,fn in (("faed col_decrypt",col_decrypt),("faed col_encrypt",col_encrypt)):
    show(label, fn(faed,KEY2))
# also dbbi with width 7 (key would need len7) - try key = first 7 of matrixsumlist? skip; 13 is the match
