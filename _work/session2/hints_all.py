import base64, hashlib, itertools, re, sys
from Crypto.Cipher import AES
W=r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work"
def load(p):
    b=base64.b64decode("".join(open(p).read().split())); return b[8:16],b[16:]
BL={"SALPH":load(W+r"\salphaseion_blob.txt"),"COSMIC":load(W+r"\cosmic_blob.txt")}
def evp(pw,salt,md):
    d=b"";pr=b""
    while len(d)<48: pr=md(pr+pw+salt).digest(); d+=pr
    return d[:32],d[32:48]
def good(pt):
    p=pt[-1]
    if not(1<=p<=16 and pt[-p:]==bytes([p])*p): return None
    b=pt[:-p]
    return b if len(b) and sum(1 for c in b if 32<=c<127 or c in(9,10,13))/len(b)>.85 else None
P=[
# 2020
"Roses are White but often Red. Yellow has a number and so does Blue. Go back to the first puzzle piece without further ado. It might have shown you only one door, beware that the rabbits nest may contain a whole lot more. Hush hush.",
"Go back to the first puzzle piece without further ado","Go back to the first puzzle piece","first puzzle piece",
"It might have shown you only one door, beware that the rabbits nest may contain a whole lot more","Hush hush",
"Humph. Hope, it is the quintessential human delusion, simultaneously the source of your greatest strength, and your greatest weakness.",
"Hope","hope is the quintessential human delusion",
"Let's see what bitcoin is worth the next halving and who knows what you'll find after opening the 2nd door. The price is in half, but what does it mean",
"2nd door","second door","The price is in half","price in half",
"Really nobody managed to find the extra door, didn't expect that after the earlier pace of cracking things.",
# 2021
"Not to give any hints but a few might not require the internet anymore.","a few might not require the internet anymore",
"Ancient spelling. One of the many many typos.","hundred FOUR = 104 is the fefefe square","fefefe is 101 010","hundred four","one hundred four","104",
"You are at the prime part already","prime part","Oh wait, shouldn't have said that. That might have been a hint.",
"Breaking salphation, should be giving the feeling of the phase's name","feeling of the phase's name","salphation","Salphation",
"R=18 A=1 B=2","R=18","1812","21","18","Could also be 21 or 1812 bit",
"SHA-256(GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)",
"There is Another DOOR","There is Another D O O R","Another DOOR","another door","THEREISANOTHERDOOR",
"The previous \"there\" is another door hint is still a thing. We're not sure if anyone has found another door so far, and we can't check that... We've seen prime numbers being mentioned; well, that is definitely an aspect which is required to proceed. Furthermore, along the way, some characters need to be 'zeroed out'.. Best of luck and happy holidays!",
"some characters need to be zeroed out","zeroed out","zero out","first day of winter","first day of winter 2021-2022",
# 2022-2024
"Cosmic Duality","cosmicduality","At least prime number is very important to get any further.","prime number is very important",
"Focussing on the theory of everything is also still a valid path to reaching the private key.","theory of everything","theoryofeverything","the theory of everything",
"yellow blue primes matrix sumlist last words before archichoice yinyang we wont give away thepassword its in front of  your eyes but youre not seeing it very last step is a true give away promised",
"yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised",
"its in front of your eyes but youre not seeing it","very last step is a true give away","true give away","promised",
"Ok ok ok ok. I can't hold this one any longer.","Are you really looking for just the btc...?","Are you really looking for just the btc","Are you really looking for just the key","look for the key","Look for the key",
"Actually, the hardest part is done.","the hardest part is done","hardest part is done",
"This may sound at little dramatic but if I suddenly can't answer you guys anymore, it was nice knowing you all","The puzzle talks for me","the puzzle talks for me",
"I'll not explain why.","Oh, and be careful of what you get yourselves into.",
"I hope that the person who connects the last pieces for the 'main price' will thus get its hands on the private key and hold or spend it wisely, but mostly enjoy it. And lastly, I hope to witness the day that the last scene of mr. Robot becomes a reality.",
"the last scene of mr. Robot","mr robot","Mr. Robot","mrrobot","main price","connects the last pieces",
"Probably the last hint: Once you hit a \"ying yang\", you'll be able to solve it the same day.","Once you hit a ying yang, you'll be able to solve it the same day","ying yang","yingyang","yin yang","yinyang","Yin Yang",
"Something was solved rather... remarkable.","salvation","Partly.","salvation part","the salvation part","Has anyone passed the salvation part",
"1357 blocks to go","1357","Happy halving everyone!",
"For those that still haven't solved the puzzle. There are few prizes to win besides the banter in this chat. A private key, some 'obscure' intel, or what I hope most of you have discovered by now, the most obvious reason to make sure you hold on to Bitcoin",
"obscure intel","some obscure intel","hold on to Bitcoin","16$ fee. Damn.","see you in 4 years","Me? No. Don't know that guy.",
# 2026
"Happy new year! Make the best of everything. Oh, and here's a \"tiny hint\" <3.","Happy new year! Make the best of everything. Oh, and here's a tiny hint <3.",
"tiny hint","a tiny hint","Make the best of everything","Happy new year","here's a tiny hint","<3",
"My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do.","NOTE: that is a hint.","that is a hint","close friends",
"The \"5\" btc was never the actual prize. That was only a tiny fraction.","The 5 btc was never the actual prize","never the actual prize","tiny fraction","a tiny fraction","held quite a secret in my head",
"I held quite a secret in my head which I seriously wanted to share with the planet... for those who can understand what I meant...",
"Jrk Bgrt","Jrk Brgt","JrkBgrt","jrkbgrt","gsmg.io","GSMG.IO","gsmg","gsmgio","hint","the first hint","our first hint is your last command","first hint","last command",
]
def variants(s):
    a=re.sub(r"[^A-Za-z0-9]","",s)
    return {s,s.lower(),s.upper(),a,a.lower(),a.upper(),re.sub(r"\s+","",s),s.strip(" .!?"),s.lower().strip(" .!?")}
bases=set()
for p in P: bases|=variants(p)
# pairs (chronological concatenation) of short phrases
short=[p for p in P if len(p)<45]
for a,b in itertools.permutations(short,2):
    bases.add(re.sub(r"[^a-z0-9]","",(a+b).lower())); bases.add(a+b); bases.add(a+" "+b)
print("bases",len(bases),file=sys.stderr)
n=0;hits=0
def sh(x): return hashlib.sha256(x).hexdigest()
for s in bases:
    b=s.encode(); h=sh(b)
    forms={s,h,h.upper(),sh(h.encode()),hashlib.md5(b).hexdigest()}
    for f in forms:
        fb=f.encode()
        for mn,md in (("sha256",hashlib.sha256),("md5",hashlib.md5)):
            for tag,(salt,ct) in BL.items():
                n+=1
                k,iv=evp(fb,salt,md)
                r=good(AES.new(k,AES.MODE_CBC,iv).decrypt(ct))
                if r: hits+=1; print("HIT",tag,mn,repr(s)[:80],repr(f)[:40],r[:200])
print("tests",n,"hits",hits)
