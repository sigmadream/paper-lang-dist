#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!t.empty() && t.back() == '\r') t.pop_back();

    std::array<int, 26> count{};

    for (char c : s) {
        ++count[c - 'a'];
    }
    for (char c : t) {
        --count[c - 'a'];
    }

    for (int x : count) {
        if (x != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}