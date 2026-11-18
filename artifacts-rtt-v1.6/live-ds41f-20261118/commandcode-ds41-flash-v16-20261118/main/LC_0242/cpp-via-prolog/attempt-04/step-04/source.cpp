#include <iostream>
#include <string>
#include <array>

int main() {
    std::string s, t;
    if (!std::getline(std::cin, s)) return 0;
    if (!std::getline(std::cin, t)) return 0;

    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!t.empty() && t.back() == '\r') t.pop_back();

    if (s.size() != t.size()) {
        std::cout << 0 << '\n';
        return 0;
    }

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