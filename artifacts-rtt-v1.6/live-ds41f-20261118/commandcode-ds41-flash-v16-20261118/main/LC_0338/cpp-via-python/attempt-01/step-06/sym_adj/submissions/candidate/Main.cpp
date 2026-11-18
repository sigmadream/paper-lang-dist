#include <iostream>
#include <vector>
#include <string>

int main() {
    long long n;
    if (!(std::cin >> n)) return 0;
    if (n < 0) n = 0;

    std::vector<int> counts(n + 1, 0);
    for (long long i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + static_cast<int>(i % 2);
    }

    std::string out;
    out.reserve((n + 1) * 7);
    for (long long i = 0; i <= n; ++i) {
        if (i) out.push_back(' ');
        out += std::to_string(counts[i]);
    }
    out.push_back('\n');
    std::cout << out;
    return 0;
}