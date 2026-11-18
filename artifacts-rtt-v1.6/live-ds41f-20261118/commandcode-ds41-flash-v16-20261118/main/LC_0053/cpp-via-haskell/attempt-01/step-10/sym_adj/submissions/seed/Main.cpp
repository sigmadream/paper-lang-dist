#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string all, tok;
    std::getline(std::cin, all);
    if (all.empty()) {
        std::string rest;
        while (std::getline(std::cin, rest)) all += "\n" + rest;
    } else {
        std::string rest;
        while (std::getline(std::cin, rest)) all += "\n" + rest;
    }

    std::istringstream iss(all);
    std::vector<long long> tokens;
    while (iss >> tok) {
        try {
            tokens.push_back(std::stoll(tok));
        } catch (...) {
            return 0;
        }
    }

    if (tokens.empty()) return 0;

    long long n = tokens[0];
    long long k = std::max(0LL, n);
    std::vector<long long> vals;
    for (long long i = 0; i < k && i + 1 < (long long)tokens.size(); ++i) {
        vals.push_back(tokens[i + 1]);
    }

    if (vals.empty()) {
        std::cout << 0 << '\n';
        return 0;
    }

    long long cur = vals[0];
    long long best = vals[0];
    for (size_t i = 1; i < vals.size(); ++i) {
        cur = std::max(vals[i], cur + vals[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}