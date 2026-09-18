#include <iostream>
#include <vector>
#include <algorithm>

bool containsDuplicate(std::vector<int>& nums) {
    std::sort(nums.begin(), nums.end());
    for (size_t i = 1; i < nums.size(); ++i) {
        if (nums[i] == nums[i - 1]) {
            return true;
        }
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
    if (containsDuplicate(nums)) {
        std::cout << 1 << std::endl;
    } else {
        std::cout << 0 << std::endl;
    }
    return 0;
}