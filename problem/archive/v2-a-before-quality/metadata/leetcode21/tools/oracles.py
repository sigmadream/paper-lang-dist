"""Two independent calculations per task; no upstream solution imports."""
from bisect import bisect_left
from collections import Counter, deque
from itertools import combinations, permutations
from math import comb


def integers(a,lo,hi):
    assert all(type(x) is int and lo<=x<=hi for x in a)


def validate(pid,args):
    a=args[0]
    limits={1:(2,10000,-10**9,10**9),121:(1,100000,0,10000),217:(1,100000,-10**9,10**9),
            53:(1,100000,-10000,10000),704:(1,10000,-9999,9999),35:(1,10000,-10000,10000),
            283:(1,10000,-2**31,2**31-1),739:(1,100000,30,100),912:(1,50000,-50000,50000)}
    if pid in limits:
        mn,mx,lo,hi=limits[pid];assert mn<=len(a)<=mx;integers(a,lo,hi)
        if pid in (1,704,35):integers([args[1]],lo,hi)
        if pid in (704,35):assert a==sorted(set(a))
        if pid==1:assert sum(a[i]+a[j]==args[1] for i,j in combinations(range(len(a)),2))==1
    elif pid in (242,387,3,139):
        if pid==3:assert 0<=len(a)<=100000 and all(32<=ord(c)<=126 for c in a)
        else:
            strings=args if pid==242 else [a]
            bound={242:50000,387:100000,139:300}[pid]
            assert all(1<=len(s)<=bound and all('a'<=c<='z' for c in s) for s in strings)
            if pid==139:
                words=args[1];assert 1<=len(words)<=1000 and len(words)==len(set(words))
                assert all(1<=len(s)<=20 and all('a'<=c<='z' for c in s) for s in words)
    elif pid==518:
        coins=args[1];integers([a],0,5000);assert 1<=len(coins)<=300 and len(coins)==len(set(coins));integers(coins,1,5000)
    elif pid==62:integers(args,1,100);assert comb(sum(args)-2,args[0]-1)<=2*10**9
    elif pid in (63,64,547):
        bound=100 if pid==63 else 200
        assert 1<=len(a)<=bound and 1<=len(a[0])<=bound and len({len(row) for row in a})==1
        integers([x for row in a for x in row],0,200 if pid==64 else 1)
        if pid==547:assert len(a)==len(a[0]) and all(a[i][i]==1 and a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a)))
    elif pid==496:
        b=args[1];assert 1<=len(a)<=len(b)<=1000 and len(a)==len(set(a)) and len(b)==len(set(b)) and set(a)<=set(b)
        integers(a+b,0,10000)
    elif pid==207:
        edges=args[1];integers([a],1,2000);assert len(edges)<=5000 and len(edges)==len(set(map(tuple,edges)))
        for edge in edges:assert len(edge)==2;integers(edge,0,a-1)
    elif pid==338:integers([a],0,100000)
    else:raise ValueError(pid)


def solve(pid,args):
    validate(pid,args);a=args[0]
    if pid==1:
        target=args[1];seen={};first=None
        for i,x in enumerate(a):
            if target-x in seen:first=[seen[target-x],i];break
            seen[x]=i
        other=next([i,j] for i,j in combinations(range(len(a)),2) if a[i]+a[j]==target)
        return first,other
    if pid==121:
        low=a[0];best=0
        for x in a:best=max(best,x-low);low=min(low,x)
        return best,max([0]+[a[j]-a[i] for i in range(len(a)) for j in range(i+1,len(a))])
    if pid==217:
        b=sorted(a);return len(set(a))!=len(a),any(x==y for x,y in zip(b,b[1:]))
    if pid==53:
        cur=best=a[0]
        for x in a[1:]:cur=max(x,cur+x);best=max(best,cur)
        return best,max(sum(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1))
    if pid in (704,35):
        target=args[1];i=bisect_left(a,target)
        if pid==35:return i,sum(x<target for x in a)
        return i if i<len(a) and a[i]==target else -1,next((i for i,x in enumerate(a) if x==target),-1)
    if pid==283:
        b=a[:];write=0
        for read in range(len(b)):
            if b[read]!=0:b[write],b[read]=b[read],b[write];write+=1
        return b,[x for x in a if x!=0]+[0]*a.count(0)
    if pid==242:return Counter(a)==Counter(args[1]),sorted(a)==sorted(args[1])
    if pid==387:
        counts=Counter(a)
        return next((i for i,x in enumerate(a) if counts[x]==1),-1),next((i for i,x in enumerate(a) if all(i==j or x!=y for j,y in enumerate(a))),-1)
    if pid==3:
        last={};start=best=0
        for i,c in enumerate(a):start=max(start,last.get(c,-1)+1);best=max(best,i-start+1);last[c]=i
        brute=max([0]+[j-i for i in range(len(a)) for j in range(i+1,len(a)+1) if len(set(a[i:j]))==j-i])
        return best,brute
    if pid==139:
        words=set(args[1]);dp=[True]+[False]*len(a)
        for i in range(1,len(a)+1):dp[i]=any(dp[j] and a[j:i] in words for j in range(i))
        def split(i):return i==len(a) or any(a[i:j] in words and split(j) for j in range(i+1,len(a)+1))
        return dp[-1],split(0)
    if pid==518:
        coins=args[1];dp=[1]+[0]*a
        for c in coins:
            for x in range(c,a+1):dp[x]+=dp[x-c]
        def counts(i,left):
            if i==len(coins):return int(left==0)
            return sum(counts(i+1,left-k*coins[i]) for k in range(left//coins[i]+1))
        assert dp[-1]<=2**31-1
        return dp[-1],counts(0,a)
    if pid==62:
        m,n=args;dp=[1]*n
        for _ in range(1,m):
            for j in range(1,n):dp[j]+=dp[j-1]
        return dp[-1],comb(m+n-2,m-1)
    if pid in (63,64):
        m,n=len(a),len(a[0]);dp=[[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if pid==63:
                    dp[i][j]=0 if a[i][j] else (1 if i==j==0 else (dp[i-1][j] if i else 0)+(dp[i][j-1] if j else 0))
                else:dp[i][j]=a[i][j]+(0 if i==j==0 else min(dp[i-1][j] if i else float('inf'),dp[i][j-1] if j else float('inf')))
        def paths(i,j):
            if i>=m or j>=n:return 0 if pid==63 else float('inf')
            if pid==63 and a[i][j]:return 0
            if i==m-1 and j==n-1:return 1 if pid==63 else a[i][j]
            if pid==63:return paths(i+1,j)+paths(i,j+1)
            return a[i][j]+min(paths(i+1,j),paths(i,j+1))
        if pid==63:assert dp[-1][-1]<=2*10**9
        return dp[-1][-1],paths(0,0)
    if pid==739:
        out=[0]*len(a);stack=[]
        for i,x in enumerate(a):
            while stack and a[stack[-1]]<x:j=stack.pop();out[j]=i-j
            stack.append(i)
        return out,[next((j-i for j in range(i+1,len(a)) if a[j]>x),0) for i,x in enumerate(a)]
    if pid==496:
        b=args[1];mapping={};stack=[]
        for x in b:
            while stack and stack[-1]<x:mapping[stack.pop()]=x
            stack.append(x)
        return [mapping.get(x,-1) for x in a],[next((y for y in b[b.index(x)+1:] if y>x),-1) for x in a]
    if pid==547:
        seen=set();count=0;n=len(a)
        for i in range(n):
            if i in seen:continue
            count+=1;stack=[i];seen.add(i)
            while stack:
                u=stack.pop()
                for v in range(n):
                    if a[u][v] and v not in seen:seen.add(v);stack.append(v)
        parent=list(range(n))
        def root(i):
            while parent[i]!=i:i=parent[i]
            return i
        for i in range(n):
            for j in range(i):
                if a[i][j]:parent[root(i)]=root(j)
        return count,len({root(i) for i in range(n)})
    if pid==207:
        n=a;edges=args[1];adj=[[] for _ in range(n)];indeg=[0]*n
        for x,y in edges:adj[y].append(x);indeg[x]+=1
        q=deque(i for i in range(n) if not indeg[i]);count=0
        while q:
            u=q.popleft();count+=1
            for v in adj[u]:
                indeg[v]-=1
                if not indeg[v]:q.append(v)
        def valid(order):
            pos={v:i for i,v in enumerate(order)}
            return all(pos[y]<pos[x] for x,y in edges)
        return count==n,any(valid(order) for order in permutations(range(n)))
    if pid==338:
        dp=[0]*(a+1)
        for i in range(1,a+1):dp[i]=dp[i//2]+i%2
        other=[]
        for i in range(a+1):
            count=0
            while i:count+=i%2;i//=2
            other.append(count)
        return dp,other
    if pid==912:
        def merge_sort(v):
            if len(v)<2:return v[:]
            l=merge_sort(v[:len(v)//2]);r=merge_sort(v[len(v)//2:]);out=[];i=j=0
            while i<len(l) and j<len(r):
                if l[i]<=r[j]:out.append(l[i]);i+=1
                else:out.append(r[j]);j+=1
            return out+l[i:]+r[j:]
        b=a[:];out=[]
        while b:x=min(b);out.append(x);b.remove(x)
        return merge_sort(a),out
    raise ValueError(pid)
