#include <iostream>
#include <string>
#include <vector>

static int parseToken(const std::string& s) {
    if (s.empty()) return 0;

    int sign = 1;
    std::size_t pos = 0;

    if (s[pos] == '+') {
        ++pos;
    } else if (s[pos] == '-') {
        sign = -1;
        ++pos;
    }

    if (pos == s.size()) return 0;

    const long long limit = 2147483648LL;
    long long value = 0;

    for (; pos < s.size(); ++pos) {
        char c = s[pos];
        if (c < '0' || c > '9') return 0;

        value = value * 10 + (c - '0');
        if (value > limit) return 0;
    }

    long long signedValue = sign * value;
    if (signedValue < -2147483648LL || signedValue > 2147483647LL) {
        return 0;
    }

    return static_cast<int>(signedValue);
}

int main() {
    std::string token;
    if (!(std::cin >> token)) {
        token = "";
    }

    int n = parseToken(token);
    if (n < 0) n = 0;

    std::vector<int> counts(n + 1, 0);

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