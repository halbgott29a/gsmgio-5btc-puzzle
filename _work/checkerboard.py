#!/usr/bin/env python3
"""Straddling-checkerboard decoder + VALIDATION against the known phase-3.2.2 VIC.
If the validation reproduces 'INCASEYOUMANAGE...', the decoder is correct and we
can trust the dbbi sweep that follows."""

def build_board(alphabet, e1, e2):
    """alphabet: 28-symbol string (letters + 2 fillers). e1<e2 escape digits.
    Returns dict: '0'..'9' -> letter (top row), and 'e1d','e2d' -> letter."""
    e1,e2=sorted((e1,e2))
    top_cols=[d for d in range(10) if d not in (e1,e2)]   # 8 columns
    board={}
    i=0
    for c in top_cols:
        board[str(c)]=alphabet[i]; i+=1
    for c in range(10):
        board[f"{e1}{c}"]=alphabet[i]; i+=1
    for c in range(10):
        board[f"{e2}{c}"]=alphabet[i]; i+=1
    return board,e1,e2

def decode(digits, alphabet, e1, e2):
    board,e1,e2=build_board(alphabet,e1,e2)
    out=[];i=0;D=digits
    while i<len(D):
        d=int(D[i])
        if d==e1 or d==e2:
            if i+1>=len(D): break
            out.append(board.get(D[i:i+2],'?')); i+=2
        else:
            out.append(board.get(D[i],'?')); i+=1
    return "".join(out)

# ---- VALIDATION: phase 3.2.2 ----
num322="15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
# README alphabet FUBCDORA.LETHINGKYMVPS.JQZXW with digit1=1,digit2=4
# dcode places the two '.' as the escape markers; convert to our 28-sym (replace . with filler)
alpha322="FUBCDORA"+"LETHINGKYM"+"VPS"  # uncertain; we'll just brute to FIND the right board
# Instead brute-force to reproduce the known plaintext to learn the exact convention:
target="INCASE"
import itertools
base="FUBCDORALETHINGKYMVPSJQZXW"   # 26 letters from the alphabet w/o dots
# try all escape pairs and a couple of fill orders
found=None
for e1,e2 in itertools.combinations(range(10),2):
    for filler in ("..","/.",".#"):
        alpha=base[:8]+base[8:18]+base[18:26]  # 26, pad to 28
        alpha28=base[:8]+filler[0]+base[8:17]+filler[1]+base[17:26]
        # try a few alphabet arrangements
        for al in (base[:28].ljust(28,'.'), (base+filler).ljust(28,'.')):
            try:
                pt=decode(num322,al,e1,e2)
            except: continue
            if pt.startswith("INCASE"):
                found=(e1,e2,al); print("MATCH conv:",e1,e2,al,"->",pt[:60])
if not found:
    print("auto-match failed; trying explicit dcode layout")
    # dcode layout: alphabet string already in board order incl 2 dots as escapes
    a="FUBCDORA.LETHINGKYMVPS.JQZXW"
    # interpret: positions of '.' give escape columns in TOP row reading
    # Build: top row reads alphabet until enough; the '.' are blanks at escape cols
    def dcode_board(a):
        # a has 28 chars incl two '.'; first 10 entries map to top row cols0-9
        top=a[:10]   # includes the two dots as blanks
        rest=a[10:].replace('.','')
        e=[i for i,ch in enumerate(top) if ch=='.']
        board={}
        for c in range(10):
            if top[c]!='.': board[str(c)]=top[c]
        k=0
        for c in range(10):
            board[f"{e[0]}{c}"]=rest[k]; k+=1
        for c in range(10):
            board[f"{e[1]}{c}"]=rest[k] if k<len(rest) else '?'; k+=1
        return board,e
    bd,e=dcode_board(a)
    def dec2(D):
        out=[];i=0
        while i<len(D):
            if int(D[i]) in e:
                out.append(bd.get(D[i:i+2],'?'));i+=2
            else:
                out.append(bd.get(D[i],'?'));i+=1
        return "".join(out)
    print("dcode-layout decode:",dec2(num322)[:80])
