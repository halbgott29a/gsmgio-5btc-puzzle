from PIL import Image
import collections
im=Image.open(r"D:\project_python\gsmgio-puzzle\gsmgio-5btc-puzzle\puzzle.png").convert("RGB")
W,H=im.size; N=14; cell=W/N     # 1048/14 = 74.857
def cls(rgb):
    r,g,b=rgb
    if r>235 and g>235 and b>235: return 'w'
    if r<40 and g<40 and b<40: return 'k'
    if b>150 and r<110: return 'b'
    if r>230 and g>230 and b<60: return 'y'
    return '?'
grid=[]
for r in range(N):
    row=""
    for c in range(N):
        x=int((c+.5)*cell); y=int((r+.5)*cell)
        row+=cls(im.getpixel((x,y)))
    grid.append(row)
print("\n".join(grid)); print(collections.Counter("".join(grid)))
# counter-clockwise inward spiral from top-left: down the left column, along the bottom (L->R), up the right column, back along the top (R->L)
g=[list(r) for r in grid]
out=[]; t,b,l,r=0,N-1,0,N-1
while t<=b and l<=r:
    for i in range(t,b+1): out.append(g[i][l])
    l+=1
    for j in range(l,r+1): out.append(g[b][j])
    b-=1
    if l<=r:
        for i in range(b,t-1,-1): out.append(g[i][r])
        r-=1
    if t<=b:
        for j in range(r,l-1,-1): out.append(g[t][j])
        t+=1
s="".join(out); print(len(s))
bits=lambda ss,bl,yl: ss.replace('k','1').replace('w','0').replace('b',bl).replace('y',yl)
for bl,yl in (('1','0'),('0','1')):
    bs=bits(s,bl,yl); by=[bs[i:i+8] for i in range(0,len(bs)-7,8)]
    print("blue=%s yellow=%s ->"%(bl,yl), "".join(chr(int(x,2)) if 32<=int(x,2)<127 else '.' for x in by), "| leftover bits:", bs[len(by)*8:])
# where do coloured cells fall in the spiral?
pos=[i for i,c in enumerate(s) if c in 'by']; print("coloured positions mod 8:",collections.Counter(p%8 for p in pos))
