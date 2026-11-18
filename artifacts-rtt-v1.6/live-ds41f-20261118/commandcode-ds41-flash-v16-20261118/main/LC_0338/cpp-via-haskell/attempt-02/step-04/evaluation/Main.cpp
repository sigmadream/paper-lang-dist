#include <iostream>
#include <string>
#include <vector>
#include <climits>
#include <cctype>

static int parseToken(const std::string& s) {
    if (s.empty()) return 0;

    std::size_t i = 0;
    int sign = 1;

    if (s[i] == '+' || s[i] == '-') {
        if (s[i] == '-') sign = -1;
        ++i;
    }

    if (i == s.size()) return 0;

    long long value = 0;
    for (; i < s.size(); ++i) {
        unsigned char ch = static_cast<unsigned char>(s[i]);
        if (!std::isdigit(ch)) return 0;

        value = value * 10 + (s[i] - '0');
        if (value > 2147483648LL) return 0;
    }

    value *= sign;
    if (value < INT_MIN || value > INT_MAX) return 0;

    return static_cast<int>(value);
}

int main() {
    std::string token;
    int n0 = 0;

    if (std::cin >> token) {
        n0 = parseToken(token);
    }

    int n = n0 < 0 ? 0 : n0;

    std::vector<int> counts(static_cast<std::size_t>(n) + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    for (int i = 0; i <= n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << counts[i];
    }
    std::cout << '\n';

    return 0;
}