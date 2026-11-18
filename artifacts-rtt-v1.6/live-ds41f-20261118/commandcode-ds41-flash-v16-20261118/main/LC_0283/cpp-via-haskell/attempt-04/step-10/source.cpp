#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> xs(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> xs[i];
    }

    std::vector<int> result;
    result.reserve(n);

    for (int x : xs) {
        if (x != 0) result.push_back(x);
    }

    for (int i = static_cast<int>(result.size()); i < n; ++i) {
        result.push_back(0);
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';

    return 0;
}