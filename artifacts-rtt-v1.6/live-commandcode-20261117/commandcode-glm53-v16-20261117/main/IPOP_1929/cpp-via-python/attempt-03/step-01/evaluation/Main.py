import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = int(data[0]), int(data[1])
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0:2] = b'\x00\x00'
    i = 2
    while i * i <= n:
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(range(i*i, n+1, i)))
        i += 1
    out = []
    for i in range(m, n + 1):
        if is_prime[i]:
            out.append(str(i))
    sys.stdout.write("\n".join(out) + "\n")

main()