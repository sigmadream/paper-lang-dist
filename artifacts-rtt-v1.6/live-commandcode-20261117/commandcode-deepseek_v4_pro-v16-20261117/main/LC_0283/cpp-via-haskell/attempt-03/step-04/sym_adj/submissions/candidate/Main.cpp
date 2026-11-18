#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> nums[i];
    }

    bool first = true;

    for (int x : nums) {
        if (x != 0) {
            if (!first) std::cout << ' ';
            std::cout << x;
            first = false;
        }
    }

    for (int x : nums) {
        if (x == 0) {
            if (!first) std::cout << ' ';
            std::cout << x;
            first = false;
        }
    }

    std::cout << '\n';
    return 0;
}