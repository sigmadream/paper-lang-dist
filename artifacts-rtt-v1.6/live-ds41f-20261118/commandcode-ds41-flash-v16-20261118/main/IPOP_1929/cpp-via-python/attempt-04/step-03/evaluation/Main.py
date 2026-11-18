import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    m = int(data[0])
    n = int(data[1])

    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0] = 0
    is_prime[1] = 0

    limit = int(n ** 0.5)
    for i in range(2, limit + 1):
        if is_prime[i]:
            start = i * i
            count = ((n - start) // i) + 1
            is_prime[start:n + 1:i] = b'\x00' * count

    result = [str(x) for x in range(m, n + 1) if is_prime[x]]
    sys.stdout.write('\n'.join(result) + '\n')

if __name__ == "__main__":
    main()