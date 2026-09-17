"""Fixed-seed functional cases and bounded scale cases; no model-output filtering."""
from random import Random

SEED = 20260917


def names(n):
    def word(value):
        chars=[]
        for _ in range(4):chars.append(chr(97+value%26));value//=26
        return 'P'+''.join(chars)
    return [word(i) for i in range(n)]


def candidates():
    result={}
    def add(pid,label,text):result.setdefault(pid,[]).append((label,text.rstrip()+'\n'))
    for pid in ('10988','1158','11729','1436','14719','1620','18870','1929','1992','2003','2110','2217','2579','2609','5567','9012','9251','9663','9935'):
        rng=Random(SEED+int(pid))
        for i in range(3):
            scale=i==2
            label='규모·수치 경계 입력' if scale else f'고정 seed 기능 입력 {i+1}'
            if pid=='10988':
                half=''.join(rng.choices('abcdefghijklmnopqrstuvwxyz',k=50 if scale else 11+i))
                value=half+half[::-1] if i!=1 else half+'z'
            elif pid=='1158':value=f'{5000 if scale else 41+i*20} {4999 if scale else 17+i*13}'
            elif pid=='11729':value=str([12,14,16][i]);label='출력 규모 증가 N='+value
            elif pid=='1436':value=str([42,1234,9999][i]);label='순위 경계 N='+value
            elif pid=='14719':
                a=[500 if j%2==0 else 0 for j in range(500)] if scale else [rng.randrange(51) for _ in range(17+i*6)]
                value=f'{500 if scale else 50} {len(a)}\n'+' '.join(map(str,a))
            elif pid=='1620':
                n=100000 if scale else 17+i*6;words=names(n)
                queries=[str((j*7919)%n+1) for j in range(n-1)]+[words[-1]] if scale else [words[rng.randrange(n)] if j%2 else str(rng.randrange(n)+1) for j in range(23)]
                value=f'{n} {len(queries)}\n'+'\n'.join(words+queries)
            elif pid=='18870':
                a=[((j*7919)%100003)-50000 for j in range(100000)] if scale else [rng.randrange(-99,100) for _ in range(19+i*4)]
                value=str(len(a))+'\n'+' '.join(map(str,a))
            elif pid=='1929':value=['101 499','10007 10999','1 100000'][i]
            elif pid=='1992':
                n=[16,32,64][i];rows=[''.join(str((x+y)%2) if scale else str(rng.randrange(2)) for x in range(n)) for y in range(n)]
                value=str(n)+'\n'+'\n'.join(rows)
            elif pid=='2003':
                a=[1]*10000 if scale else [rng.randrange(1,10) for _ in range(17+i*4)]
                value=f'{len(a)} {5000 if scale else 23+i*7}\n'+' '.join(map(str,a))
            elif pid=='2110':
                a=list(range(399998,-1,-2)) if scale else rng.sample(range(1000),9+i)
                value=f'{len(a)} {100001 if scale else 4+i}\n'+'\n'.join(map(str,a))
            elif pid=='2217':
                a=[j%10000+1 for j in range(100000)] if scale else [rng.randrange(1,10001) for _ in range(11+i)]
                value=str(len(a))+'\n'+'\n'.join(map(str,a))
            elif pid=='2579':
                a=[rng.randrange(1,10001) for _ in range(300 if scale else 19+i)]
                value=str(len(a))+'\n'+'\n'.join(map(str,a))
            elif pid=='2609':value=['9991 9973','8192 4096','9998 9996'][i]
            elif pid=='5567':
                n=500 if scale else 17+i*4
                edges=[(x,y) for x in range(1,n+1) for y in range(x+1,n+1)]
                edges=rng.sample(edges,10000 if scale else 31+i*7)
                value=f'{n}\n{len(edges)}\n'+'\n'.join(f'{x} {y}' for x,y in edges)
            elif pid=='9012':
                # Lengths 24, 26 and 48 avoid all original individual public strings.
                width=[24,26,48][i];count=128 if scale else 7
                strings=[''.join(rng.choices('()',k=width)) for _ in range(count)]
                strings[0]='('*((width//2)-1)+'()'+')'*((width//2)-1)
                value=str(count)+'\n'+'\n'.join(strings)
            elif pid=='9251':
                n=1000 if scale else 12+i
                value=''.join(rng.choices('ABCDE',k=n))+'\n'+''.join(rng.choices('ABCDE',k=n))
            elif pid=='9663':value=str(12+i);label='남은 유효 보드 크기 N='+value
            elif pid=='9935':
                value='ab'*500000+'\nab' if scale else ''.join(rng.choices('abcd',k=43+i*6))+'\nabc'
            add(pid,label,value)
    return result
