#include <iostream>
#include <string>
#include <vector>
#include <climits>

static bool isTrimChar(unsigned char c) {
    return c <= ' ';
}

static bool isCppSpaceAscii(unsigned char c) {
    return c == ' ' || c == '\t' || c == '\n' ||
           c == '\v' || c == '\f' || c == '\r';
}

static bool parseJavaInt(const std::string& s, int& result) {
    if (s.empty()) return false;

    std::size_t i = 0;
    bool neg = false;

    if (s[i] == '+' || s[i] == '-') {
        neg = s[i] == '-';
        ++i;
        if (i == s.size()) return false;
    }

    long long v = 0;
    long long limit = neg ? 2147483648LL : 2147483647LL;

    for (; i < s.size(); ++i) {
        char c = s[i];
        if (c < '0' || c > '9') return false;

        int d = c - '0';
        if (v > (limit - d) / 10) return false;
        v = v * 10 + d;
    }

    if (neg) {
        if (v == 2147483648LL) result = INT_MIN;
        else result = static_cast<int>(-v);
    } else {
        result = static_cast<int>(v);
    }

    return true;
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    std::size_t start = 0;
    std::size_t end = line.size();

    while (start < end && isTrimChar(static_cast<unsigned char>(line[start]))) ++start;
    while (end > start && isTrimChar(static_cast<unsigned char>(line[end - 1]))) --end;

    std::string trimmed = line.substr(start, end - start);
    if (trimmed.empty()) return 0;

    std::size_t tokenEnd = 0;
    while (tokenEnd < trimmed.size() &&
           !isCppSpaceAscii(static_cast<unsigned char>(trimmed[tokenEnd]))) {
        ++tokenEnd;
    }

    std::string token = trimmed.substr(0, tokenEnd);
    int n;
    if (!parseJavaInt(token, n)) return 0;
    if (n < 0) return 0;

    std::vector<int> counts(n + 1);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::string output;
    output.reserve((n + 1) * 7);

    for (int i = 0; i <= n; ++i) {
        if (i > 0) output.push_back(' ');
        output += std::to_string(counts[i]);
    }
    output.push_back('\n');

    std::cout << output;
    return 0;
}