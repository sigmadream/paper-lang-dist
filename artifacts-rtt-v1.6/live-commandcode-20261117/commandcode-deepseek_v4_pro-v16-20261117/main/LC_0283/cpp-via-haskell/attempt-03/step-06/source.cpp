#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> nums[i];
    }

    std::vector<int> result;
    result.reserve(n);

    for (int x : nums) {
        if (x != 0) result.push_back(x);
    }

    int zeroCount = n - static_cast<int>(result.size());
    for (int i = 0; i < zeroCount; ++i) {
        result.push_back(0);
    }

    for (std::size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';

    return 0;
}