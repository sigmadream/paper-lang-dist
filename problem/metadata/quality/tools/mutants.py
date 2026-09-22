"""Eight deliberately faulty implementations, a diagnostic panel, not a coverage score."""
from collections import Counter


def int16(x):
    return (x+32768)%65536-32768


def narrow_kadane(text):
    a=list(map(int,text.split()))[1:];cur=best=a[0]
    for x in a[1:]:cur=max(x,int16(cur+x));best=max(best,cur)
    return str(best)


def limited_unique_scan(text):
    s=text.removesuffix('\n');counts=Counter(s)
    return str(next((i for i,c in enumerate(s[:256]) if counts[c]==1),-1))


def narrow_wait_distance(text):
    a=list(map(int,text.split()))[1:];out=[0]*len(a);stack=[]
    for i,x in enumerate(a):
        while stack and a[stack[-1]]<x:j=stack.pop();out[j]=(i-j)%65536
        stack.append(i)
    return ' '.join(map(str,out))


def limited_sort_buffer(text):
    return ' '.join(map(str,sorted(list(map(int,text.split()))[1:1025])))


def trim_string_input(text):
    s=text.strip();last={};left=best=0
    for i,c in enumerate(s):left=max(left,last.get(c,-1)+1);best=max(best,i-left+1);last[c]=i
    return str(best)


def narrow_coordinate_rank(text):
    a=list(map(int,text.split()))[1:];rank={x:int16(i) for i,x in enumerate(sorted(set(a)))}
    return ' '.join(str(rank[x]) for x in a)


def narrow_stair_sum(text):
    a=[0]+list(map(int,text.split()))[1:];n=len(a)-1;dp=[0]*(n+1);dp[1]=a[1]
    if n>1:dp[2]=int16(a[1]+a[2])
    for i in range(3,n+1):dp[i]=int16(max(dp[i-2],int16(dp[i-3]+a[i-1]))+a[i])
    return str(dp[n])


def limited_window_buffer(text):
    tokens=list(map(int,text.split()));target=tokens[1];a=tokens[2:66];left=total=count=0
    for x in a:
        total+=x
        while total>target:total-=a[left];left+=1
        count+=total==target
    return str(count)


PANEL = [
    ('LC_0053','signed-16-bit-accumulator',narrow_kadane),
    ('LC_0387','scan-only-first-256-characters',limited_unique_scan),
    ('LC_0739','unsigned-16-bit-distance',narrow_wait_distance),
    ('LC_0912','1024-element-input-buffer',limited_sort_buffer),
    ('LC_0003','trim-meaningful-whitespace',trim_string_input),
    ('IPOP_18870','signed-16-bit-rank',narrow_coordinate_rank),
    ('IPOP_2579','signed-16-bit-dp-sum',narrow_stair_sum),
    ('IPOP_2003','64-element-input-buffer',limited_window_buffer),
]
