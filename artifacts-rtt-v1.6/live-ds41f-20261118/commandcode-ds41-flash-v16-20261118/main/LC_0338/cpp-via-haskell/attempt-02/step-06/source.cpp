#include <iostream>
#include <string>
#include <vector>

static int parseToken(const std::string& s) {
    int sign = 1;
    std::string rest;

    if (s.empty()) {
        rest = "";
    } else if (s[0] == '+') {
        sign = 1;
        rest = s.substr(1);
    } else if (s[0] == '-') {
        sign = -1;
        rest = s.substr(1);
    } else {
        sign = 1;
        rest = s;
    }

    if (rest.empty()) return 0;

    long long val = 0;
    const long long limit = 2147483648LL;

    for (char c : rest) {
        if (c < '0' || c > '9') return 0;
        long long nv = val * 10 + (c - '0');
        if (nv > limit) return 0;
        val = nv;
    }

    long long v = static_cast<long long>(sign) * val;
    if (v < -2147483648LL || v > 2147483647LL) return 0;
    return static_cast<int>(v);
}

int main() {
    std::string token;
    if (!(std::cin >> token)) token = "";

    int n0 = parseToken(token);
    int n = (n0 < 0) ? 0 : n0;

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