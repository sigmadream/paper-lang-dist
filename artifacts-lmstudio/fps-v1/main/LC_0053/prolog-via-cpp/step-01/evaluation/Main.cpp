#include <iostream>
#include <vector>
#include <algorithm>

int kadane(const std::vector<int>& nums) {
    int max_current = nums[0];
    int max_global = nums[0];
    for (size_t i = 1; i < nums.size(); ++i) {
        max_current = std::max(nums[i], max_current + nums[i]);
        if (max_current > max_global) {
            max_global = max_current;
        }
    }
    return max_global;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> nums[i];
    }
    std::cout << kadane(nums) << std::endl;
    return 0;
}