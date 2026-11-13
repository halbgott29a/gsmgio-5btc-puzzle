import sys,re,hashlib,base64,itertools
sys.path.insert(0,'.')
exec(open('phase0.py').read().split("# where do coloured")[0].replace("print(","(lambda *a,**k:None)("))
G=[list(r) for r in grid]; N=14
isP=lambda n:n>1 and all(n%i for i in range(2,int(n**.5)+1))
# --- numeric series
url="gsmg.io/theseedisplanted"
Yb=[k+1 for k,ch in enumerate(url) if ord(ch)%2==0]; Bb=[k+1 for k,ch in enumerate(url) if ord(ch)%2==1]
spiral_idx=lambda ks:[8*(k-1)+7 for k in ks]
cells={'y':[(r,c) for r in range(N) for c in range(N) if G[r][c]=='y'],'b':[(r,c) for r in range(N) for c in range(N) if G[r][c]=='b']}
SER={}
SER["yellow_byte#"]=Yb; SER["blue_byte#"]=Bb
SER["yellow_prime_byte#"]=[v for v in Yb if isP(v)]; SER["blue_prime_byte#"]=[v for v in Bb if isP(v)]
SER["yellow_spiral_idx"]=spiral_idx(Yb); SER["blue_spiral_idx"]=spiral_idx(Bb)
SER["yellow_spiral_idx_prime"]=[v for v in SER["yellow_spiral_idx"] if isP(v)]; SER["blue_spiral_idx_prime"]=[v for v in SER["blue_spiral_idx"] if isP(v)]
SER["yellow_rc_raster"]=[r*N+c for r,c in cells['y']]; SER["blue_rc_raster"]=[r*N+c for r,c in cells['b']]
SER["yellow_rc_raster_prime"]=[v for v in SER["yellow_rc_raster"] if isP(v)]; SER["blue_rc_raster_prime"]=[v for v in SER["blue_rc_raster"] if isP(v)]
SER["yellow_row"]=[r+1 for r,c in cells['y']]; SER["yellow_col"]=[c+1 for r,c in cells['y']]
SER["blue_row"]=[r+1 for r,c in cells['b']]; SER["blue_col"]=[c+1 for r,c in cells['b']]
bit=lambda ch:1 if ch in 'kb' else 0
SER["rowsum_bits"]=[sum(bit(x) for x in row) for row in G]; SER["colsum_bits"]=[sum(bit(G[r][c]) for r in range(N)) for c in range(N)]
bit2=lambda ch:1 if ch=='k' else 0
SER["rowsum_black"]=[sum(bit2(x) for x in row) for row in G]; SER["colsum_black"]=[sum(bit2(G[r][c]) for r in range(N)) for c in range(N)]
SER["rowcount_yellow"]=[row.count('y') for row in G]; SER["colcount_yellow"]=[sum(G[r][c]=='y' for r in range(N)) for c in range(N)]
SER["rowcount_blue"]=[row.count('b') for row in G]; SER["colcount_blue"]=[sum(G[r][c]=='b' for r in range(N)) for c in range(N)]
SER["counts_9_15"]=[9,15]; SER["counts_9_15_24"]=[9,15,24]
SER["spiral_sum_by_byte"]=[sum(bit(s[8*k+j]) for j in range(8)) for k in range(24)]   # popcount of each URL byte
SER["byte_values"]=[ord(ch) for ch in url]
SER["byte_values_prime"]=[ord(ch) for ch in url if isP(ord(ch))]
if __name__=="__main__":
    for k,v in SER.items(): print(f"{k:26s}",v)
