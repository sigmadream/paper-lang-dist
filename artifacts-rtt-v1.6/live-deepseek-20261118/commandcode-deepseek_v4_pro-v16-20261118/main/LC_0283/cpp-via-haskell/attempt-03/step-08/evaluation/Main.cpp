#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> nums[i];
    }

    std::vector<int> result;
    result.reserve(n);

    for (int x : nums) {
        if (x != 0) result.push_back(x);
    }
    for (int x : nums) {
        if (x == 0) result.push_back(x);
    }

    for (std::size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';

    return 0;
}