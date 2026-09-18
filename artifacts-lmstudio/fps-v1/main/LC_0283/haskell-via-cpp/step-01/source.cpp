#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;
    std::vector<int> xs(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> xs[i];
    }
    
    int nonzero_count = 0;
    for (int i = 0; i < n; ++i) {
        if (xs[i] != 0) {
            std::swap(xs[nonzero_count++], xs[i]);
        }
    }

    for (int i = 0; i < n; ++i) {
        std::cout << xs[i];
        if (i < n - 1) std::cout << " ";
    }
    std::cout << std::endl;

    return 0;
}