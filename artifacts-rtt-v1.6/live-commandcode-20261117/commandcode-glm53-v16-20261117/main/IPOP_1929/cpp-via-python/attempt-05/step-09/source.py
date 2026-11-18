import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = int(data[0]), int(data[1])
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0:2] = b'\x00\x00' if n >= 1 else b'\x00'
    i = 2
    while i * i <= n:
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
        i += 1
    out = []
    for k in range(m, n + 1):
        if is_prime[k]:
            out.append(str(k))
    sys.stdout.write('\n'.join(out) + '\n')

main()