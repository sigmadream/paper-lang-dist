#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;
    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> nums[i])) return 0;
    }

    // Move all zeros to the end while preserving the relative order of non-zero elements
    std::stable_partition(nums.begin(), nums.end(), [](int x) { return x != 0; });

    for (int i = 0; i < n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << nums[i];
    }
    std::cout << '\n';
    return 0;
}