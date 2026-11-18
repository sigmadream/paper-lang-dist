#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!std::getline(std::cin, s)) return 0;
    if (!std::getline(std::cin, t)) return 0;

    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!t.empty() && t.back() == '\r') t.pop_back();

    if (s.size() != t.size()) {
        std::cout << 0 << '\n';
        return 0;
    }

    std::array<int, 256> cnt{};
    for (unsigned char c : s) ++cnt[c];
    for (unsigned char c : t) --cnt[c];

    for (int v : cnt) {
        if (v != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}