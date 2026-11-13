import sys,re
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
L=open(r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work\chat_transcript.txt",encoding='utf8',errors='ignore').read().split('\n')
blocks=[];i=0
while i<len(L):
    if L[i].startswith('=== ['):
        j=i+1; body=[]
        while j<len(L) and not L[j].startswith('=== ['): body.append(L[j]); j+=1
        m=re.match(r'=== \[(\d\d)\.(\d\d)\.(\d{4}) (\d\d:\d\d):\d\d [^\]]*\] (.*)',L[i])
        if m: blocks.append((f"{m.group(3)}-{m.group(2)}-{m.group(1)}",m.group(4),m.group(5),' '.join(x for x in body if x.strip())))
        i=j
    else: i+=1
def show(day,t0="00:00",t1="23:59",who=None,maxc=240,kw=None):
    for d,t,n,x in blocks:
        if d==day and t0<=t<=t1 and (who is None or who in n) and (kw is None or re.search(kw,x,re.I)):
            print(f"{t} {n[:12]:12s}: {x[:maxc]}")
