import sys

def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return
    m, n = int(data[0]), int(data[1])

    is_prime = bytearray([1]) * (n + 1)
    if n >= 0:
        is_prime[0] = 0
    if n >= 1:
        is_prime[1] = 0

    i = 2
    while i * i <= n:
        if is_prime[i]:
            is_prime[i * i:n + 1:i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1

    out = []
    for x in range(m, n + 1):
        if is_prime[x]:
            out.append(str(x))
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))

main()