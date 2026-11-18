#include <iostream>
#include <string>
#include <cctype>

static std::string strip_cr(const std::string& s) {
    if (!s.empty() && s.back() == '\r') return s.substr(0, s.size() - 1);
    return s;
}

static std::string trim(const std::string& s) {
    size_t b = 0, e = s.size();
    while (b < e && std::isspace(static_cast<unsigned char>(s[b]))) ++b;
    while (e > b && std::isspace(static_cast<unsigned char>(s[e - 1]))) --e;
    return s.substr(b, e - b);
}

static bool valid_parentheses(const std::string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            ++bal;
        } else if (c == ')') {
            if (bal <= 0) return false;
            --bal;
        } else {
            return false;
        }
    }
    return bal == 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!std::getline(std::cin, first)) return 0;

    std::string tstr = trim(first);
    if (tstr.empty()) return 0;

    int T = 0;
    try {
        T = std::stoi(tstr);
    } catch (...) {
        return 0;
    }

    for (int i = 0; i < T; ++i) {
        std::string line;
        if (!std::getline(std::cin, line)) return 0;
        line = strip_cr(line);
        std::cout << (valid_parentheses(line) ? "YES" : "NO") << '\n';
    }

    return 0;
}