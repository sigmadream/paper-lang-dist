#include <iostream>
#include <vector>
#include <string>

int countOnes(int n) {
    int count = 0;
    while (n > 0) {
        count += n % 2;
        n /= 2;
    }
    return count;
}

int main() {
    int n;
    std::cin >> n;
    for (int i = 0; i <= n; ++i) {
        std::cout << countOnes(i);
        if (i < n) std::cout << " ";
    }
    std::cout << std::endl;
    return 0;
}