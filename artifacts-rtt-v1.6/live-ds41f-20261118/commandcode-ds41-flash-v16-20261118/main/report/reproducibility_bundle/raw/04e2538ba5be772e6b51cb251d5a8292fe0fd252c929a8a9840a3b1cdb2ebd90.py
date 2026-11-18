import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    m = int(data[0])
    n = int(data[1])

    is_prime = bytearray(b'\x01') * (n + 1)
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
    for x in range(m, n + 1):
        if is_prime[x]:
            out.append(str(x))
    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()