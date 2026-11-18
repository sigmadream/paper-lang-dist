#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> result;
    result.reserve(n);
    int zeroCount = 0;
    for (int i = 0; i < n; ++i) {
        int x;
        std::cin >> x;
        if (x == 0) {
            ++zeroCount;
        } else {
            result.push_back(x);
        }
    }
    for (int i = 0; i < zeroCount; ++i) result.push_back(0);

    for (int i = 0; i < n; ++i) {
        if (i) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';
    return 0;
}