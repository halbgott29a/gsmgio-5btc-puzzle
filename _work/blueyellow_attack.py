#!/usr/bin/env python3
from Crypto.Cipher import AES
"""FORMALIZED 'Blue/Yellow = First Hint' attack.
Derive candidate keys from the 24 byte-boundary blue/yellow squares (+ primes),
then test each as: (a) AES password for both blobs, (b) checkerboard alphabet to
decode dbbi (with hill-climb refinement), (c) a-i->digit permutation."""
import base64, hashlib, itertools, re, random, math, collections, os
random.seed(0)

# ---------- inputs ----------
URL="gsmg.io/theseedisplanted"
COLORS="BBBBYBBBYYBBBBYBBYYBYYBY"   # per-char color at byte boundary (B=blue=1, Y=yellow=0)
assert len(URL)==len(COLORS)==24
blue_pos=[i+1 for i,c in enumerate(COLORS) if c=='B']     # 1..24
yellow_pos=[i+1 for i,c in enumerate(COLORS) if c=='Y']
bluechars="".join(URL[i] for i,c in enumerate(COLORS) if c=='B')
yellowchars="".join(URL[i] for i,c in enumerate(COLORS) if c=='Y')
bits_b1="".join('1' if c=='B' else '0' for c in COLORS)
bits_b0="".join('0' if c=='B' else '1' for c in COLORS)
def isp(n): return n>1 and all(n%k for k in range(2,int(n**.5)+1))
prime_idx=[i for i in range(1,25) if isp(i)]
prime_chars="".join(URL[i-1] for i in prime_idx)
prime_colors="".join(COLORS[i-1] for i in prime_idx)

dbbi="dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe"

# ---------- candidate KEYS ----------
KEYS={
 "colorbits_b1":bits_b1, "colorbits_b0":bits_b0,
 "bluechars":bluechars, "yellowchars":yellowchars,
 "blue+yellow":bluechars+yellowchars, "yellow+blue":yellowchars+bluechars,
 "bluepos":"".join(map(str,blue_pos)), "yellowpos":"".join(map(str,yellow_pos)),
 "primechars":prime_chars, "primecolors_bits":"".join('1' if c=='B' else '0' for c in prime_colors),
 "hexb1":format(int(bits_b1,2),'06x'), "hexb0":format(int(bits_b0,2),'06x'),
 "numb1":str(int(bits_b1,2)), "numb0":str(int(bits_b0,2)),
 "url_uniq":"".join(dict.fromkeys(URL.replace('.','').replace('/',''))),
}
# add sha256 of each key as a derived key too
for k in list(KEYS):
    KEYS["sha("+k+")"]=hashlib.sha256(KEYS[k].encode()).hexdigest()

# ---------- (a) AES test ----------
def load(p):
    b=base64.b64decode("".join(open(p).read().split()));return b[8:16],b[16:]
blobs={"COSMIC":load(r"D:\tmp\gsmgio-5btc-puzzle\ChatExport\files\cd.b64.txt"),"SALPH":load("salphaseion_blob.txt")}
def evp(pw,salt,md,kl=32,il=16):
    d=b"";pr=b""
    while len(d)<kl+il: pr=md(pr+pw+salt).digest();d+=pr
    return d[:kl],d[kl:kl+il]
def good(pt):
    p=pt[-1]
    if 1<=p<=16 and pt[-p:]==bytes([p])*p:
        b=pt[:-p]
        if b and sum(1 for c in b if 32<=c<127 or c in(9,10,13))/len(b)>0.85: return b
    return None
aes_hits=0
for kn,kv in KEYS.items():
    for f in {kv,hashlib.sha256(kv.encode()).hexdigest()}:
        for tg,(salt,ct) in blobs.items():
            for md in (hashlib.sha256,hashlib.md5):
                k,iv=evp(f.encode(),salt,md)
                b=good(AES.new(k,AES.MODE_CBC,iv).decrypt(ct))
                if b: print(f"[+++AES {tg}] key={kn} -> {b[:120]!r}");aes_hits+=1
print(f"(a) AES: {aes_hits} hits over {len(KEYS)} keys")

# ---------- (b) checkerboard alphabet from key, decode dbbi + hillclimb ----------
from cb2 import decode as cbdecode
corpus=""
for p in [r"D:\tmp\gsmgio-5btc-puzzle\README.md"]:
    if os.path.exists(p): corpus+=open(p,encoding="utf-8",errors="replace").read()
corpus=re.sub(r'[^A-Za-z]','',corpus).upper()
tri=collections.Counter(corpus[i:i+3] for i in range(len(corpus)-2)); tot=sum(tri.values()); fl=math.log(0.01/tot)
def fit(s):
    s=re.sub(r'[^A-Z]','',s.upper())
    if len(s)<3: return -1e9
    return sum(math.log(tri[s[i:i+3]]/tot) if s[i:i+3] in tri else fl for i in range(len(s)-2))/(len(s)-2)
def pad28(seed):
    s="".join(dict.fromkeys(re.sub(r'[^A-Za-z]','',seed).upper()))
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if ch not in s: s+=ch
    s=s[:26]; return s[:8]+"."+s[8:17]+"."+s[17:26]
maps={"a0i8":{c:str(i) for i,c in enumerate("abcdefghi")},"a1i9":{c:str(i+1) for i,c in enumerate("abcdefghi")}}
cb_best=[]
for kn,kv in KEYS.items():
    al=pad28(kv)
    if len(al)!=28: continue
    for mn,mp in maps.items():
        dig="".join(mp[c] for c in dbbi)
        for e1,e2 in [(1,4),(2,5)]:
            out=cbdecode(dig,al,e1,e2)
            cb_best.append((fit(out),f"{kn}/{mn}/e{e1}{e2}",out))
cb_best.sort(reverse=True)
print(f"\n(b) checkerboard via blue/yellow keys - top 6 (real english fit~-7.9):")
for f,l,s in cb_best[:6]: print(f"  [{f:.2f}] {l:30} {s[:46]}")

# ---------- (c) a-i mapping from yellow (9 yellows <-> 9 symbols) ----------
# yellow_pos has 9 entries -> rank them to a permutation, map onto a-i
print("\n(c) a-i mapping from 9 yellow positions:")
print("  yellow_pos(9):",yellow_pos,"  blue_pos(15):",blue_pos)
# map a..i to the rank-order of yellow positions
order=sorted(range(9),key=lambda i:yellow_pos[i])
ai_map={"abcdefghi"[i]:str((order.index(i)%9)+1) for i in range(9)}
dig_c="".join(ai_map[c] for c in dbbi)
for e1,e2 in [(1,4),(2,5)]:
    print(f"  yellow-rank map, 3.2.2 alpha, e{e1}{e2}:",cbdecode(dig_c,"FUBCDORA.LETHINGKYMVPS.JQZXW",e1,e2)[:46])
print(f"\nSummary: blue/yellow data: bits={bits_b1} bluechars={bluechars!r} yellowchars={yellowchars!r}")
print(f"  url unique(13)={KEYS['url_uniq']!r}  primechars={prime_chars!r}")
