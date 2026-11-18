#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s >> t)) return 0;

    std::array<int, 26> counts{};

    for (char ch : s) {
        ++counts[ch - 'a'];
    }
    for (char ch : t) {
        --counts[ch - 'a'];
    }

    bool valid = true;
    for (int c : counts) {
        if (c != 0) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}