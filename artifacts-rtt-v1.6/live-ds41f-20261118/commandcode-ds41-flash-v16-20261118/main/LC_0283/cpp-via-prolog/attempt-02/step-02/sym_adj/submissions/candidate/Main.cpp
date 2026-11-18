#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) {
        std::cout << '\n';
        return 0;
    }

    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> nums[i];
    }

    std::vector<int> result;
    result.reserve(n);

    int zeroCount = 0;
    for (int x : nums) {
        if (x == 0) {
            ++zeroCount;
        } else {
            result.push_back(x);
        }
    }

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