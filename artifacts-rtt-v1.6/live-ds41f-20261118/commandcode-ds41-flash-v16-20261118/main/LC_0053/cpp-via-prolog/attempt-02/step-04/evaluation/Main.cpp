#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N;
    if (!(std::cin >> N)) return 0;

    std::vector<long long> nums(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> nums[i];
    }

    if (N == 0) return 0;

    long long best = nums[0];
    long long cur = nums[0];
    for (int i = 1; i < N; ++i) {
        cur = std::max<long long>(nums[i], cur + nums[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}