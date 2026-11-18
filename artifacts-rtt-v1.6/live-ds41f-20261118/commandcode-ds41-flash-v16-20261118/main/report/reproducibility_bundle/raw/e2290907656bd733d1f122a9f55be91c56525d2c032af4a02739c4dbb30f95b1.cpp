#include <iostream>
#include <string>
#include <array>

static void strip_cr(std::string& s) {
    if (!s.empty() && s.back() == '\r') {
        s.pop_back();
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;

    if (!std::getline(std::cin, s)) {
        return 0;
    }
    if (!std::getline(std::cin, t)) {
        return 0;
    }

    strip_cr(s);
    strip_cr(t);

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

    for (int v : count) {
        if (v != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}