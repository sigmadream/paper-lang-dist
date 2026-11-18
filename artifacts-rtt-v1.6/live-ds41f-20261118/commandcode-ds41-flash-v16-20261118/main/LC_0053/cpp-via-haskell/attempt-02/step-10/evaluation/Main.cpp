#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

static bool parseFirstToken(const std::string& s, bool& neg, unsigned long long& mag) {
    if (s.empty()) return false;

    std::size_t i = 0;
    neg = false;
    if (s[0] == '+' || s[0] == '-') {
        neg = (s[0] == '-');
        i = 1;
    }

    if (i >= s.size()) return false;

    unsigned long long v = 0;
    const unsigned long long CAP = 3000000000ULL;

    for (; i < s.size(); ++i) {
        unsigned char c = static_cast<unsigned char>(s[i]);
        if (!std::isdigit(c)) return false;

        int d = s[i] - '0';
        if (v < CAP) {
            v = v * 10ULL + static_cast<unsigned long long>(d);
            if (v > CAP) v = CAP;
        }
    }

    mag = v;
    return true;
}

static bool parseValue(const std::string& s, long long& out) {
    if (s.empty()) return false;

    std::size_t i = 0;
    bool neg = false;

    if (s[0] == '+' || s[0] == '-') {
        neg = (s[0] == '-');
        i = 1;
    }

    if (i >= s.size()) return false;

    long long v = 0;

    for (; i < s.size(); ++i) {
        unsigned char c = static_cast<unsigned char>(s[i]);
        if (!std::isdigit(c)) return false;

        int d = s[i] - '0';
        v = v * 10LL + static_cast<long long>(d);
    }

    out = neg ? -v : v;
    return true;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!(std::cin >> first)) return 0;

    bool neg = false;
    unsigned long long mag = 0;

    if (!parseFirstToken(first, neg, mag)) return 0;

    long long k;
    if (neg || mag == 0) {
        k = 0;
    } else {
        const unsigned long long LIMIT = 2147483647ULL;
        k = static_cast<long long>(std::min(mag, LIMIT));
    }

    std::vector<long long> nums;
    bool invalid = false;

    for (long long i = 0; i < k; ++i) {
        std::string tok;
        if (!(std::cin >> tok)) break;

        long long v;
        if (!parseValue(tok, v)) {
            invalid = true;
            break;
        }

        nums.push_back(v);
    }

    if (invalid) {
        nums.clear();
    }

    long long answer;

    if (nums.empty()) {
        answer = 0;
    } else {
        long long current = nums[0];
        long long best = nums[0];

        for (std::size_t i = 1; i < nums.size(); ++i) {
            long long y = nums[i];
            current = std::max(y, current + y);
            best = std::max(best, current);
        }

        answer = best;
    }

    std::cout << answer << '\n';
    return 0;
}