import math

def sieve_of_eratosthenes(m, n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    for i in range(m, n + 1):
        if is_prime[i]:
            print(i)

if __name__ == "__main__":
    m, n = map(int, input().split())
    
    sieve_of_eratosthenes(m, n)
