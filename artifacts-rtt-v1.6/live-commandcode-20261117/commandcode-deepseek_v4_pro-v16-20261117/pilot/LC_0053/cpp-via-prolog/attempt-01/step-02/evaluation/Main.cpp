#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int N;
    if (!(std::cin >> N)) return 0;
    std::vector<int> nums(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> nums[i];
    }
    int cur = nums[0];
    int best = nums[0];
    for (int i = 1; i < N; ++i) {
        cur = std::max(nums[i], cur + nums[i]);
        best = std::max(best, cur);
    }
    std::cout << best << '\n';
    return 0;
}