import sys

def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return
    m, n = map(int, data[:2])

    is_prime = bytearray(b'\x01') * (n + 1)
    if n >= 0:
        is_prime[0] = 0
    if n >= 1:
        is_prime[1] = 0

    i = 2
    while i * i <= n:
        if is_prime[i]:
            start = i * i
            is_prime[start:n + 1:i] = b'\x00' * (((n - start) // i) + 1)
        i += 1

    out = []
    for x in range(m, n + 1):
        if is_prime[x]:
            out.append(str(x))

    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()