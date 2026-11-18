import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = int(data[0]), int(data[1])
    sieve = bytearray([1]) * (n + 1)
    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0
    i = 2
    while i * i <= n:
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
        i += 1
    out = []
    for i in range(m, n + 1):
        if sieve[i]:
            out.append(str(i))
    sys.stdout.write('\n'.join(out))
    if out:
        sys.stdout.write('\n')

main()