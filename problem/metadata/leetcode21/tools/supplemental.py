"""Three predeclared additions per task; independent of model-generated code."""
from random import Random

SEED = 20260917


def cases():
    result = {}
    for pid in (1,121,217,53,704,35,283,242,387,3,139,518,62,63,64,739,496,547,207,338,912):
        rng = Random(SEED + pid)
        rows = []
        for i in range(2):
            n = 17 + i * 6
            if pid == 1:
                a = rng.sample(range(10,400),n);a.insert(3,-1000)
                args = [a,-1000+a[-2]]
            elif pid == 121:args = [[rng.randrange(10001) for _ in range(n)]]
            elif pid in (217,53,283,912):args = [[rng.randrange(-17,18) for _ in range(n)]]
            elif pid in (704,35):args = [sorted(rng.sample(range(-500,500),n)),rng.randrange(-500,500)]
            elif pid == 242:
                s=''.join(rng.choices('abcdef',k=n));t=list(s);rng.shuffle(t)
                if i:t[-1]='z'
                args=[s,''.join(t)]
            elif pid == 387:args=[''.join(rng.choices('abcdef',k=n))+'z']
            elif pid == 3:args=[' ab ' if i==0 else 'a  b']
            elif pid == 139:args=[''.join(rng.choices('ab',k=19+i)),['a','ab','ba','bbb']]
            elif pid == 518:args=[41+i*12,rng.sample(range(2,16),3)]
            elif pid == 62:args=[[4,13],[7,9]][i]
            elif pid in (63,64):args=[[[rng.randrange(4)==0 if pid==63 else rng.randrange(201) for _ in range(5+i)] for _ in range(4)]];args=[[[int(x) for x in row] for row in args[0]]]
            elif pid == 739:args=[[rng.randrange(30,101) for _ in range(n)]]
            elif pid == 496:
                b=rng.sample(range(10001),n);args=[rng.sample(b,7),b]
            elif pid == 547:
                g=[[int(x==y) for y in range(13+i)] for x in range(13+i)]
                for x in range(len(g)):
                    for y in range(x):g[x][y]=g[y][x]=int(rng.random()<0.15)
                args=[g]
            elif pid == 207:
                edges=[[x,y] for x in range(7) for y in range(x) if rng.random()<0.35]
                if i:edges.extend([[0,6],[6,0]])
                args=[7,sorted(set(map(tuple,edges)))];args[1]=[list(e) for e in args[1]]
            elif pid == 338:args=[127 if i==0 else 1023]
            rows.append((f'고정 seed 기능 입력 {i+1}',args))
        if pid==1:large=[[-1,0]+list(range(2,10000)),-1]
        elif pid==121:large=[[i%10001 for i in range(100000)]]
        elif pid==217:large=[list(range(99999))+[49999]]
        elif pid==53:large=[[10000]*100000]
        elif pid==704:large=[list(range(-9999,10000,2)),9999]
        elif pid==35:large=[list(range(-10000,10000,2)),9999]
        elif pid==283:large=[[-2**31,0,2**31-1,0]*2500]
        elif pid==242:
            s=('abcdefghijklmnopqrstuvwxyz'*1924)[:50000];large=[s,s[::-1]]
        elif pid==387:large=['a'*99999+'b']
        elif pid==3:large=[(''.join(chr(x) for x in range(32,127))*1053)[:100000]]
        elif pid==139:large=['a'*299+'b',['a'*i for i in range(1,21)]]
        elif pid==518:large=[4999,list(range(2,42,2))]
        elif pid==62:large=[17,18]
        elif pid==63:large=[[[0]*100 for _ in range(99)]+[[1]*100]]
        elif pid==64:large=[[[((i*71+j*43)%201) for j in range(200)] for i in range(200)]]
        elif pid==739:large=[[70]*99999+[71]]
        elif pid==496:large=[list(range(999,-1,-1)),list(range(1000))]
        elif pid==547:large=[[[int(i==j or abs(i-j)==1) for j in range(200)] for i in range(200)]]
        elif pid==207:large=[2000,[[i+1,i] for i in range(1999)]+[[0,1999]]]
        elif pid==338:large=[65535]
        elif pid==912:large=[[((i*7919)%100001)-50000 for i in range(50000)]]
        result[pid]=rows+[('규모·수치 경계 입력',large)]
    return result
