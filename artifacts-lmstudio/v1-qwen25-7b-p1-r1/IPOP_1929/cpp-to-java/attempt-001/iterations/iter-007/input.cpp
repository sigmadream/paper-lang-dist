#include <iostream>
#include <vector>

int main() {
    int m, n;
    std::cin >> m >> n;
    
    std::vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;
    
    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    
    for (int i = m; i <= n; i++) {
        if (isPrime[i]) {
            std::cout << i << std::endl;
        }
    }
    
    return 0;
}
