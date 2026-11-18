#include <iostream>
#include <vector>

int main() {
    std::vector<int> tokens;
    int val;
    while (std::cin >> val) {
        tokens.push_back(val);
    }

    if (tokens.empty()) return 0;

    int n = tokens[0];
    std::vector<int> nums(tokens.begin() + 1, tokens.begin() + 1 + n);

    std::vector<int> nonZeros, zeros;
    for (int x : nums) {
        if (x != 0) nonZeros.push_back(x);
        else zeros.push_back(x);
    }

    bool first = true;
    for (int x : nonZeros) {
        if (!first) std::cout << ' ';
        std::cout << x;
        first = false;
    }
    for (int x : zeros) {
        if (!first) std::cout << ' ';
        std::cout << x;
        first = false;
    }
    std::cout << '\n';

    return 0;
}