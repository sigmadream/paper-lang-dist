#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string ns;
    if (!(std::cin >> ns)) return 0;

    int n;
    try {
        n = std::stoi(ns);
    } catch (...) {
        return 0;
    }

    std::string firstToken;
    if (!(std::cin >> firstToken)) return 0;

    long long first;
    try {
        first = std::stoll(firstToken);
    } catch (...) {
        return 0;
    }

    long long cur = first;
    long long best = first;

    for (int i = 1; i < n; i++) {
        std::string token;
        if (!(std::cin >> token)) break;

        long long x;
        try {
            x = std::stoll(token);
        } catch (...) {
            break;
        }

        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}