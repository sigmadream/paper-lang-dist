#include <iostream>
#include <string>
#include <array>

int main() {
    std::string s, t;
    std::cin >> s >> t;

    std::array<int, 26> counts{};
    for (char ch : s) {
        counts[ch - 'a']++;
    }
    for (char ch : t) {
        counts[ch - 'a']--;
    }

    for (int x : counts) {
        if (x != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }
    std::cout << 1 << '\n';
    return 0;
}