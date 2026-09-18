#include <iostream>
#include <vector>

int countOnes(int n) {
    int count = 0;
    while (n > 0) {
        count += n % 2;
        n /= 2;
    }
    return count;
}

int main() {
    int N;
    std::cin >> N;
    std::vector<int> result(N + 1);
    for (int i = 0; i <= N; ++i) {
        result[i] = countOnes(i);
    }
    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << " ";
        std::cout << result[i];
    }
    std::cout << std::endl;
    return 0;
}