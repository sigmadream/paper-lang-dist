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

    int ending_here = nums[0], best_so_far = nums[0];
    for (size_t i = 1; i < N; ++i) {
        ending_here = std::max(nums[i], ending_here + nums[i]);
        best_so_far = std::max(best_so_far, ending_here);
    }

    std::cout << best_so_far << std::endl;
    return 0;
}