import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return

    M = int(data[0])
    N = int(data[1])

    is_prime = bytearray(b'\x01') * (N + 1)
    is_prime[0] = 0
    if N >= 1:
        is_prime[1] = 0

    for i in range(2, math.isqrt(N) + 1):
        if is_prime[i]:
            is_prime[i * i:N + 1:i] = b'\x00' * (((N - i * i) // i) + 1)

    primes = [str(x) for x in range(M, N + 1) if is_prime[x]]
    if primes:
        sys.stdout.write('\n'.join(primes) + '\n')

if __name__ == "__main__":
    main()