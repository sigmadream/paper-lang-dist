#include <iostream>
#include <vector>
#include <algorithm>

bool hasDuplicate(const std::vector<int>& nums) {
    if (nums.size() <= 1) return false;
    std::vector<int> sortedNums(nums);
    std::sort(sortedNums.begin(), sortedNums.end());
    for (size_t i = 0; i < sortedNums.size() - 1; ++i) {
        if (sortedNums[i] == sortedNums[i + 1]) return true;
    }
    return false;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> nums[i];
    }
    if (hasDuplicate(nums)) {
        std::cout << 1 << std::endl;
    } else {
        std::cout << 0 << std::endl;
    }
    return 0;
}