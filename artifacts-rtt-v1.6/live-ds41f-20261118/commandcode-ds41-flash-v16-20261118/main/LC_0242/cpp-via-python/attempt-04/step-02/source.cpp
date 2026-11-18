#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    std::cin >> s >> t;

    std::array<int, 26> counts{};
    for (char ch : s) {
        ++counts[ch - 'a'];
    }
    for (char ch : t) {
        --counts[ch - 'a'];
    }

    for (int count : counts) {
        if (count != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}