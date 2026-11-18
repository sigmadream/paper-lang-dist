#include <iostream>
#include <string>
#include <array>

static bool readLine(std::string& line) {
    if (!std::getline(std::cin, line)) return false;
    if (!line.empty() && line.back() == '\r') {
        line.pop_back();
    }
    return true;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!readLine(s) || !readLine(t)) {
        std::cout << 0 << '\n';
        return 0;
    }

    if (s.size() != t.size()) {
        std::cout << 0 << '\n';
        return 0;
    }

    std::array<int, 26> counts{};
    for (std::size_t i = 0; i < s.size(); ++i) {
        ++counts[s[i] - 'a'];
        --counts[t[i] - 'a'];
    }

    for (int c : counts) {
        if (c != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}