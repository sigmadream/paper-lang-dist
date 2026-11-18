#include <iostream>
#include <string>
#include <vector>

static bool parseJavaInt(const std::string& s, int& out) {
    if (s.empty()) return false;

    size_t i = 0;
    bool neg = false;
    if (s[i] == '+' || s[i] == '-') {
        neg = (s[i] == '-');
        ++i;
        if (i == s.size()) return false;
    }

    long long val = 0;
    const long long limit = neg ? 2147483648LL : 2147483647LL;

    for (; i < s.size(); ++i) {
        char c = s[i];
        if (c < '0' || c > '9') return false;

        int digit = c - '0';
        if (val > (limit - digit) / 10) return false;
        val = val * 10 + digit;
    }

    if (neg) {
        long long signedVal = -val;
        if (signedVal < -2147483648LL) return false;
        out = static_cast<int>(signedVal);
    } else {
        if (val > 2147483647LL) return false;
        out = static_cast<int>(val);
    }

    return true;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    size_t start = 0;
    size_t end = line.size();

    while (start < end &&
           (line[start] == ' ' || line[start] == '\t' ||
            line[start] == '\r' || line[start] == '\n')) {
        ++start;
    }

    while (end > start &&
           (line[end - 1] == ' ' || line[end - 1] == '\t' ||
            line[end - 1] == '\r' || line[end - 1] == '\n')) {
        --end;
    }

    if (start >= end) return 0;

    std::string trimmed = line.substr(start, end - start);

    int n;
    if (!parseJavaInt(trimmed, n)) return 0;
    if (n < 0) return 0;

    std::vector<int> counts(n + 1, 0);

    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::string result;

    for (int i = 0; i <= n; ++i) {
        if (i > 0) result.push_back(' ');
        result += std::to_string(counts[i]);
    }

    result.push_back('\n');

    std::cout << result;

    return 0;
}