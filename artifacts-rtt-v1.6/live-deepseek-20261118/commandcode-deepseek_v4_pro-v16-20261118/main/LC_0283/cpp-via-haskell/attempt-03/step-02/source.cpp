#include <iostream>
#include <vector>

int main() {
    int N;
    if (!(std::cin >> N)) return 0;

    std::vector<int> nums(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> nums[i];
    }

    std::vector<int> result;
    result.reserve(N);
    int zeroCount = 0;
    for (int x : nums) {
        if (x != 0) result.push_back(x);
        else ++zeroCount;
    }
    for (int i = 0; i < zeroCount; ++i) {
        result.push_back(0);
    }

    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';
    return 0;
}