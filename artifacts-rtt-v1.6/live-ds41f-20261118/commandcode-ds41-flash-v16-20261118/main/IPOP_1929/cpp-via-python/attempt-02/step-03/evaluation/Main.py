import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return

    m = int(data[0])
    n = int(data[1])

    is_prime = bytearray(b'\x01') * (n + 1)

    if n >= 0:
        is_prime[0] = 0
    if n >= 1:
        is_prime[1] = 0

    limit = math.isqrt(n)
    for i in range(2, limit + 1):
        if is_prime[i]:
            start = i * i
            count = (n - start) // i + 1
            is_prime[start:n + 1:i] = b'\x00' * count

    primes = [str(i) for i in range(m, n + 1) if is_prime[i]]
    if primes:
        sys.stdout.write('\n'.join(primes) + '\n')

if __name__ == "__main__":
    main()