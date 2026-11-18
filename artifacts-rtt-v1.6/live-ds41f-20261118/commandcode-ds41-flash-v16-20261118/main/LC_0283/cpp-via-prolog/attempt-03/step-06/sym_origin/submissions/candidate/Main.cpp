#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> values;
    values.reserve(n > 0 ? static_cast<std::size_t>(n) : 0);

    for (int i = 0; i < n; ++i) {
        int x;
        std::cin >> x;
        values.push_back(x);
    }

    bool first = true;
    for (int x : values) {
        if (x != 0) {
            if (!first) {
                std::cout << ' ';
            }
            std::cout << x;
            first = false;
        }
    }

    for (int x : values) {
        if (x == 0) {
            if (!first) {
                std::cout << ' ';
            }
            std::cout << x;
            first = false;
        }
    }

    std::cout << '\n';
    return 0;
}