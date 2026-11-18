#include <iostream>
#include <vector>
#include <string>

int main() {
    long long n;
    if (!(std::cin >> n)) return 0;
    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }
    std::string out;
    out.reserve((n + 1) * 2);
    for (int i = 0; i <= n; ++i) {
        if (i > 0) out.push_back(' ');
        out += std::to_string(counts[i]);
    }
    out.push_back('\n');
    std::cout << out;
    return 0;
}