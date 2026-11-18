#include <iostream>
#include <string>
#include <array>

int main() {
    std::string s, t;
    std::cin >> s >> t;

    std::array<int, 26> counts{};

    for (char c : s) {
        ++counts[c - 'a'];
    }

    for (char c : t) {
        --counts[c - 'a'];
    }

    bool valid = true;
    for (int count : counts) {
        if (count != 0) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}