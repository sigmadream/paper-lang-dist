#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;
    if (n == 0) return 0;

    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> nums[i])) return 0;
    }

    int cur = nums[0];
    int best = nums[0];
    for (int i = 1; i < n; ++i) {
        int x = nums[i];
        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}