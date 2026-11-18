#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s) || !(std::cin >> t)) {
        std::cout << "0\n";
        return 0;
    }

    if (s.size() != t.size()) {
        std::cout << "0\n";
        return 0;
    }

    std::array<int, 26> cnt{};
    for (char c : s) ++cnt[c - 'a'];
    for (char c : t) --cnt[c - 'a'];

    for (int x : cnt) {
        if (x != 0) {
            std::cout << "0\n";
            return 0;
        }
    }

    std::cout << "1\n";
    return 0;
}