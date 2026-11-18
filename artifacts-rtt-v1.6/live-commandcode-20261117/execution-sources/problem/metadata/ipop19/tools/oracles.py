"""Independent small-input oracles; no imported repository solution code."""
from collections import deque
from functools import lru_cache
from itertools import combinations
from math import gcd, isqrt
from bisect import bisect_left
from collections import Counter


def solve(problem, text):
    """Return two independently obtained answers, or validate a constructive one."""
    t = text.split()
    if problem == '10988':
        s = t[0]
        assert 1 <= len(s) <= 100 and s.isascii() and s.isalpha() and s.islower()
        return str(int(s == s[::-1])), str(int(all(s[i] == s[-i-1] for i in range(len(s)//2))))
    if problem == '1158':
        n, k = map(int, t)
        assert 1 <= k <= n <= 5000
        a, order, i = list(range(1, n+1)), [], 0
        while a:
            i = (i+k-1) % len(a)
            order.append(a.pop(i))
        q, other = deque(range(1, n+1)), []
        while q:
            q.rotate(-(k-1))
            other.append(q.popleft())
        fmt = lambda a: '<' + ', '.join(map(str, a)) + '>'
        return fmt(order), fmt(other)
    if problem == '11729':
        n = int(t[0]); assert len(t) == 1 and 1 <= n <= 20
        moves = []
        def visit(k, a, b, c):
            if k:
                visit(k-1, a, c, b); moves.append((a,c)); visit(k-1, b,a,c)
        visit(n,1,2,3)
        pegs = {1:list(range(n,0,-1)),2:[],3:[]}
        for a,b in moves:
            assert pegs[a]
            d = pegs[a].pop()
            assert not pegs[b] or pegs[b][-1] > d
            pegs[b].append(d)
        assert pegs[3] == list(range(n,0,-1)) and not pegs[1] and not pegs[2]
        assert len(moves) == 2**n-1  # Lower bound and legality, independent of recursion.
        output = str(len(moves))+'\n'+'\n'.join(f'{a} {b}' for a,b in moves)
        return output, output
    if problem == '1436':
        n = int(t[0]); assert len(t) == 1 and 1 <= n <= 10000
        seen, value = 0, 665
        while seen < n:
            value += 1
            seen += '666' in str(value)
        # Independent enumeration by location of a fixed substring, then deduplication.
        candidates = set()
        for suffix_len in range(len(str(value))-2):
            scale = 10**suffix_len
            for prefix in range(value//(1000*scale)+1):
                base = (prefix*1000+666)*scale
                if base > value: continue
                candidates.update(range(base, min(base+scale, value+1)))
        return str(value), str(sorted(candidates)[n-1])
    if problem == '14719':
        h,w = map(int,t[:2]); a = list(map(int,t[2:]))
        assert 1 <= h <= 500 and 1 <= w <= 500 and len(a)==w and all(0<=x<=h for x in a)
        first = sum(max(0,min(max(a[:i+1]),max(a[i:]))-a[i]) for i in range(w))
        second = 0
        for level in range(1,h+1):
            walls = [i for i,x in enumerate(a) if x>=level]
            if walls: second += sum(a[i]<level for i in range(walls[0],walls[-1]+1))
        return str(first), str(second)
    if problem == '1620':
        n,m = map(int,t[:2]); names=t[2:2+n]; queries=t[2+n:]
        assert 1<=n<=100000 and 1<=m<=100000 and len(queries)==m and len(set(names))==n
        assert all(2<=len(s)<=20 and s.isascii() and s.isalpha() and
                   ((s[0].isupper() and s[1:].islower()) or (s[-1].isupper() and s[:-1].islower())) for s in names)
        mapping = {str(i+1):s for i,s in enumerate(names)} | {s:str(i+1) for i,s in enumerate(names)}
        assert all(q in mapping for q in queries)
        a='\n'.join(mapping[q] for q in queries)
        b='\n'.join(names[int(q)-1] if q.isdigit() else str(names.index(q)+1) for q in queries)
        return a,b
    if problem == '18870':
        n=int(t[0]); a=list(map(int,t[1:])); assert len(a)==n and 1<=n<=1000000 and all(abs(x)<=10**9 for x in a)
        rank={v:i for i,v in enumerate(sorted(set(a)))}
        distinct=sorted(set(a))
        return ' '.join(str(rank[x]) for x in a), ' '.join(str(bisect_left(distinct,x)) for x in a)
    if problem == '1929':
        lo,hi=map(int,t); assert 1<=lo<=hi<=1000000
        flags=bytearray(b'\1')*(hi+1); flags[0:2]=b'\0\0'
        for k in range(2,isqrt(hi)+1):
            if flags[k]: flags[k*k:hi+1:k]=b'\0'*len(range(k*k,hi+1,k))
        a=[x for x in range(lo,hi+1) if flags[x]]
        b=[x for x in range(lo,hi+1) if x>=2 and all(x%d for d in range(2,isqrt(x)+1))]
        assert a, 'BOJ 1929 requires at least one prime'
        return '\n'.join(map(str,a)), '\n'.join(map(str,b))
    if problem == '1992':
        n=int(t[0]); rows=t[1:]; assert 1<=n<=64 and n&(n-1)==0 and len(rows)==n and all(len(r)==n and set(r)<=set('01') for r in rows)
        def rec(y,x,size):
            cells={rows[j][i] for j in range(y,y+size) for i in range(x,x+size)}
            if len(cells)==1:return cells.pop()
            d=size//2
            return '('+''.join(rec(j,i,d) for j,i in ((y,x),(y,x+d),(y+d,x),(y+d,x+d)))+')'
        layer=[list(r) for r in rows]
        while len(layer)>1:
            new=[]
            for y in range(0,len(layer),2):
                line=[]
                for x in range(0,len(layer),2):
                    c=[layer[y][x],layer[y][x+1],layer[y+1][x],layer[y+1][x+1]]
                    line.append(c[0] if c[0] in ('0','1') and len(set(c))==1 else '('+''.join(c)+')')
                new.append(line)
            layer=new
        return rec(0,0,n),layer[0][0]
    if problem == '2003':
        n,target=map(int,t[:2]); a=list(map(int,t[2:]))
        assert len(a)==n and 1<=n<=10000 and 1<=target<=300000000 and all(1<=x<=30000 for x in a)
        l=total=count=0
        for x in a:
            total+=x
            while total>target:total-=a[l];l+=1
            count+=total==target
        if n<=30:brute=sum(sum(a[i:j])==target for i in range(n) for j in range(i+1,n+1))
        else:
            prefixes=Counter({0:1});prefix=brute=0
            for x in a:prefix+=x;brute+=prefixes[prefix-target];prefixes[prefix]+=1
        return str(count),str(brute)
    if problem == '2110':
        n,k=map(int,t[:2]); a=sorted(map(int,t[2:]))
        assert len(a)==len(set(a))==n and 2<=k<=n<=200000 and 0<=a[0]<=a[-1]<=10**9
        lo,hi=1,a[-1]-a[0]
        while lo<=hi:
            d=(lo+hi)//2; count=1; last=a[0]
            for x in a[1:]:
                if x-last>=d:count+=1;last=x
            if count>=k:lo=d+1
            else:hi=d-1
        if n<=20:brute=max(min(b[i+1]-b[i] for i in range(k-1)) for b in combinations(a,k))
        else:
            # Large supplemental cases use a uniform lattice: packing gives an exact bound.
            gap=a[1]-a[0];assert all(y-x==gap for x,y in zip(a,a[1:]))
            brute=((n-1)//(k-1))*gap
        return str(hi),str(brute)
    if problem == '2217':
        n=int(t[0]); a=list(map(int,t[1:])); assert len(a)==n and 1<=n<=100000 and all(1<=x<=10000 for x in a)
        first=max(x*(n-i) for i,x in enumerate(sorted(a)))
        if n<=20:other=max(min(b)*len(b) for k in range(1,n+1) for b in combinations(a,k))
        else:
            freq=Counter(a);count=other=0
            for weight in range(10000,0,-1):count+=freq[weight];other=max(other,weight*count)
        return str(first),str(other)
    if problem == '2579':
        n=int(t[0]); a=[0]+list(map(int,t[1:])); assert len(a)==n+1 and 1<=n<=300 and all(1<=x<=10000 for x in a[1:])
        dp=[0]*(n+1);dp[1]=a[1]
        if n>=2:dp[2]=a[1]+a[2]
        for i in range(3,n+1):dp[i]=max(dp[i-2],dp[i-3]+a[i-1])+a[i]
        @lru_cache(None)
        def routes(pos,consecutive):
            if pos==n:return 0
            options=[]
            if pos+1<=n and consecutive<2:options.append(a[pos+1]+routes(pos+1,consecutive+1))
            if pos+2<=n:options.append(a[pos+2]+routes(pos+2,1))
            return max(options,default=-10**9)
        return str(dp[n]),str(routes(0,0))
    if problem == '2609':
        a,b=map(int,t);assert 1<=a<=10000 and 1<=b<=10000
        g=gcd(a,b); div=max(x for x in range(1,min(a,b)+1) if a%x==b%x==0)
        multiple=next(x for x in range(max(a,b),a*b+1,max(a,b)) if x%a==x%b==0)
        return f'{g}\n{a*b//g}',f'{div}\n{multiple}'
    if problem == '5567':
        n,m=map(int,t[:2]); vals=list(map(int,t[2:]));edges=list(zip(vals[::2],vals[1::2]))
        assert len(vals)==2*m and 2<=n<=500 and 1<=m<=10000 and len(set(edges))==m and all(1<=a<b<=n for a,b in edges)
        adj=[set() for _ in range(n+1)]
        for a,b in edges:adj[a].add(b);adj[b].add(a)
        dist={1:0}; q=deque([1])
        while q:
            u=q.popleft()
            if dist[u]==2:continue
            for v in adj[u]:
                if v not in dist:dist[v]=dist[u]+1;q.append(v)
        other={v for v in range(2,n+1) if v in adj[1] or any(v in adj[u] for u in adj[1])}
        return str(len(dist)-1),str(len(other))
    if problem == '9012':
        n=int(t[0]);strings=t[1:]; assert n==len(strings) and n>=1 and all(2<=len(s)<=50 and set(s)<=set('()') for s in strings)
        out=[];other=[]
        for s in strings:
            balance=0;valid=True
            for c in s:
                balance+=1 if c=='(' else -1
                if balance<0:valid=False
            out.append('YES' if valid and balance==0 else 'NO')
            while '()' in s:s=s.replace('()','')
            other.append('YES' if not s else 'NO')
        return '\n'.join(out),'\n'.join(other)
    if problem == '9251':
        a,b=t;assert 1<=len(a)<=1000 and 1<=len(b)<=1000 and all(s.isascii() and s.isalpha() and s.isupper() for s in (a,b))
        dp=[0]*(len(b)+1)
        for x in a:
            prev=0
            for j,y in enumerate(b,1):
                old=dp[j];dp[j]=prev+1 if x==y else max(dp[j],dp[j-1]);prev=old
        if min(len(a),len(b))>20:
            masks={}
            for i,c in enumerate(b):masks[c]=masks.get(c,0)|(1<<i)
            state=0
            for c in a:
                x=state|masks.get(c,0);state=x&~(x-((state<<1)|1))
            return str(dp[-1]),str(state.bit_count())
        short,long=sorted((a,b),key=len)
        best=0
        for mask in range(1<<len(short)):
            sub=''.join(x for i,x in enumerate(short) if mask>>i&1)
            it=iter(long)
            if len(sub)>best and all(any(y==x for y in it) for x in sub):best=len(sub)
        return str(dp[-1]),str(best)
    if problem == '9663':
        n=int(t[0]);assert len(t)==1 and 1<=n<15
        full=(1<<n)-1
        def bit(cols,left,right):
            if cols==full:return 1
            choices=full&~(cols|left|right);count=0
            while choices:
                p=choices&-choices;choices-=p
                count+=bit(cols|p,(left|p)<<1,(right|p)>>1)
            return count
        def backtrack(row,cols,d1,d2):
            if row==n:return 1
            return sum(backtrack(row+1,cols|{c},d1|{row+c},d2|{row-c}) for c in range(n) if c not in cols and row+c not in d1 and row-c not in d2)
        # Published independent counts, OEIS A000170 (checked 2026-09-17).
        # Small boards retain the independently implemented set-based search.
        other={12:14200,13:73712,14:365596}[n] if n>=12 else backtrack(0,set(),set(),set())
        return str(bit(0,0,0)),str(other)
    if problem == '9935':
        s,b=t; assert 1<=len(s)<=1000000 and 1<=len(b)<=36 and len(set(b))==len(b) and all(x.isascii() and x.isalnum() for x in (s,b))
        stack=[]
        for c in s:
            stack.append(c)
            if len(stack)>=len(b) and ''.join(stack[-len(b):])==b:del stack[-len(b):]
        other=s
        while b in other:other=other.replace(b,'')
        return ''.join(stack) or 'FRULA',other or 'FRULA'
    raise ValueError(problem)


METHODS = {
 '10988':('문자열 역순 비교','대칭 위치 전수 비교'),
 '1158':('리스트 인덱스 제거','deque 회전 시뮬레이션'),
 '11729':('재귀 이동열 생성','모든 이동의 합법성·최종 상태·2^N-1 최소 이동 수 검사'),
 '1436':('정수 순회와 문자열 검색','666의 자릿수 위치별 후보 생성·집합 중복 제거'),
 '14719':('열별 좌우 최대 높이','높이별 수평 빈칸 계수'),
 '1620':('양방향 사전','리스트 직접 탐색'),
 '18870':('정렬 고유값 순위','각 값보다 작은 고유값 완전 계수'),
 '1929':('에라토스테네스 체','각 수의 제곱근까지 나눗셈 검사'),
 '1992':('영역 재귀 분할','단일 픽셀에서 2x2 상향 병합'),
 '2003':('양수 배열 투 포인터','모든 연속 구간 완전탐색'),
 '2110':('최소 거리 이분탐색·탐욕 배치','공유기 위치 조합 완전탐색'),
 '2217':('정렬 후 중량 임계값','모든 비어 있지 않은 로프 부분집합'),
 '2579':('점화식 DP','합법적인 계단 이동 경로 완전탐색'),
 '2609':('유클리드 GCD와 곱/GCD','약수·공배수 직접 순회'),
 '5567':('깊이 2 BFS','길이 1·2 경로 직접 검사'),
 '9012':('접두 합과 최종 균형','인접 괄호 쌍 반복 제거'),
 '9251':('행 단위 LCS DP','짧은 문자열의 모든 부분수열 검사'),
 '9663':('비트마스크 배치 탐색','열·대각선 집합을 이용한 배치 탐색'),
 '9935':('스택 접미사 제거','문자열 전체 치환 반복'),
}

METHODS.update({
 '18870': ('정렬 고유값 순위 사전','고유값 배열의 이분탐색 위치'),
 '2003': ('양수 배열 투 포인터','소형 구간 전수 탐색 / 대형 누적합 빈도'),
 '2110': ('최소 거리 이분탐색·탐욕 배치','소형 배치 조합 전수 탐색 / 대형 균등 격자 배치 상한 공식'),
 '2217': ('정렬 후 중량 임계값','소형 부분집합 전수 탐색 / 대형 중량 빈도 누적'),
 '2579': ('점화식 DP','메모이제이션을 사용한 합법 이동 상태 탐색'),
 '9251': ('행 단위 LCS DP','소형 부분수열 전수 탐색 / 대형 비트셋 LCS'),
 '9663': ('비트마스크 배치 탐색','N<=11 집합 기반 탐색 / N=12..14 OEIS A000170의 독립 공개 계수'),
})
