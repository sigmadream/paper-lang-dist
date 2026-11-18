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
        ++count[static_cast<unsigned char>(c) - 'a'];
    }
    for (char c : t) {
        --count[static_cast<unsigned char>(c) - 'a'];
    }

    for (int v : count) {
        if (v != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}