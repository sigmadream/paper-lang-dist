#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int N;
    std::cin >> N;
    std::vector<int> nums(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> nums[i];
    }
    
    auto it = std::remove(nums.begin(), nums.end(), 0);
    std::fill(it, nums.end(), 0);
    
    for (int num : nums) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    return 0;
}