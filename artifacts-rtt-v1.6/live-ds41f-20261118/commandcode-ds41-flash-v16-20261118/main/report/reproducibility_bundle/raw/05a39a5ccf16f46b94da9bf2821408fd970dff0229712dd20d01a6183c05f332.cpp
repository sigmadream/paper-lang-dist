#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> xs;
    xs.reserve(n);
    for (int i = 0; i < n; ++i) {
        int x;
        std::cin >> x;
        xs.push_back(x);
    }

    std::vector<int> result;
    result.reserve(n);
    for (int x : xs) {
        if (x != 0) result.push_back(x);
    }
    while (static_cast<int>(result.size()) < n) {
        result.push_back(0);
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';

    return 0;
}