import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = int(data[0]), int(data[1])
    is_prime = bytearray([1]) * (n + 1)
    is_prime = bytearray(n + 1)
    for i in range(n + 1):
        is_prime[i] = 1
    if n >= 0:
        is_prime[0] = 0
    if n >= 1:
        is_prime[1] = 0
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = 0
        i += 1
    out = []
    for k in range(m, n + 1):
        if is_prime[k]:
            out.append(str(k))
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))

main()