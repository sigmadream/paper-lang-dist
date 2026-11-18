#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> vals(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> vals[i];
    }

    std::vector<int> result;
    result.reserve(n);

    int zeroCount = 0;
    for (int x : vals) {
        if (x == 0) {
            ++zeroCount;
        } else {
            result.push_back(x);
        }
    }

    result.insert(result.end(), zeroCount, 0);

    for (std::size_t i = 0; i < result.size(); ++i) {
        if (i > 0) {
            std::cout << ' ';
        }
        std::cout << result[i];
    }
    std::cout << '\n';

    return 0;
}