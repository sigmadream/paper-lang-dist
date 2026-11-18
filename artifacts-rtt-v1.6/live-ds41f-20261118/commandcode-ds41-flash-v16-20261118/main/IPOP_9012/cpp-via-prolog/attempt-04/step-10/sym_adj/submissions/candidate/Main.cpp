#include <iostream>
#include <string>
#include <cctype>

static bool is_ws(int c) {
    return c == 9 || c == 10 || c == 11 || c == 12 || c == 13 || c == 32;
}

static std::string trim(const std::string& s) {
    std::size_t l = 0;
    std::size_t r = s.size();
    while (l < r && is_ws(static_cast<unsigned char>(s[l]))) ++l;
    while (r > l && is_ws(static_cast<unsigned char>(s[r - 1]))) --r;
    return s.substr(l, r - l);
}

static bool parse_int(const std::string& s, long long& value) {
    if (s.empty()) return false;
    std::size_t i = 0;
    if (s[i] == '+' || s[i] == '-') ++i;
    if (i == s.size()) return false;
    for (std::size_t j = i; j < s.size(); ++j) {
        if (!std::isdigit(static_cast<unsigned char>(s[j]))) return false;
    }
    try {
        value = std::stoll(s);
    } catch (...) {
        return false;
    }
    return true;
}

static bool valid_parens(const std::string& s) {
    long long balance = 0;
    for (char ch : s) {
        if (ch == '(') {
            ++balance;
        } else if (ch == ')') {
            if (balance <= 0) return false;
            --balance;
        }
    }
    return balance == 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!std::getline(std::cin, first)) return 0;

    std::string trimmed = trim(first);
    long long t = 0;
    if (!parse_int(trimmed, t)) return 0;

    if (t <= 0) return 0;

    for (long long i = 0; i < t; ++i) {
        std::string line;
        if (!std::getline(std::cin, line)) break;
        std::string s = trim(line);
        std::cout << (valid_parens(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}