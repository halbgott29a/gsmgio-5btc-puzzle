import sys,itertools,random,collections
sys.path.insert(0,'.')
exec(open('phase0.py').read().split("# counter-clockwise")[0].replace("print(","(lambda *a,**k:None)("))
# trusted grid = published transcription (it reproduces the URL); add the FEFEFE cell
notebook='''00110b0010110y
11b1001110b011
1101110b001001
0110b000011101
0b1000110y0110
100110y010y011
100b1100010y00
b11000000010y0
00011b0111110b
11b111y0110001
1101000y011011
11110010b01100
0b0111010y0110
01b0110110b011'''.split('\n')
nb=[[{'0':'w','1':'k','b':'b','y':'y'}[ch] for ch in row] for row in notebook]
nb[7][4]='f'   # FEFEFE cell (row 7, col 4)
diff=[(r,c,grid[r][c],nb[r][c]) for r in range(14) for c in range(14) if grid[r][c]!=nb[r][c]]
print("cells where my pixel sampling != transcription:",diff)
raw=open(r"D:\project_python\gsmgio-puzzle\halbgott29a-fork\_work\salph_raw.txt").read().strip()
dbbi=raw[:91]; D=[ "abcdefghi".index(c) for c in dbbi]
classes=['k','w','b','y','f']
def tri(M,kind,order):
    out=[]
    pairs=[(i,j) for i in range(14) for j in range(i+1,14)] if order=="row" else [(i,j) for j in range(14) for i in range(j)]
    if kind.startswith("lower"): pairs=[(j,i) for i,j in pairs]
    return pairs
random.seed(3)
best=[]
for perm in itertools.permutations(range(5)):
    val=dict(zip(classes,perm))
    M=[[val[x] for x in row] for row in nb]
    for order in ("row","col"):
        P=tri(M,"upper",order)
        for opname,op in (("sum",lambda a,b:a+b),("absdiff",lambda a,b:abs(a-b)),("a(upper)",lambda a,b:a),("b(lower)",lambda a,b:b),("sum mod9 +1",lambda a,b:(a+b+1)%9)):
            seq=[op(M[i][j],M[j][i]) for i,j in P]
            for shift in (0,1):
                m=sum(1 for x,y in zip(seq,D) if x==y+ (shift and 0))  # direct
                best.append((m,perm,order,opname))
best.sort(reverse=True)
print("chance level ~",91/9)
for b in best[:6]: print(b)
# null: shuffle dbbi
nul=[]
for _ in range(300):
    Ds=D[:]; random.shuffle(Ds)
    mx=0
    for perm in random.sample(list(itertools.permutations(range(5))),20):
        val=dict(zip(classes,perm)); M=[[val[x] for x in row] for row in nb]
        P=tri(M,"upper","row"); seq=[M[i][j]+M[j][i] for i,j in P]; mx=max(mx,sum(1 for x,y in zip(seq,Ds) if x==y))
    nul.append(mx)
print("null max matches (shuffled dbbi, 20 perms):",max(nul),"mean",sum(nul)/len(nul))
