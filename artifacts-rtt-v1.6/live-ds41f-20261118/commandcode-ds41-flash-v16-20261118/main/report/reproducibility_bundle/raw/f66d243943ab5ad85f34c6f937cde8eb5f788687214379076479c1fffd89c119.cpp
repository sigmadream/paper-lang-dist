#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::string sb;
    for (int i = 0; i <= n; ++i) {
        if (i > 0) sb += ' ';
        sb += std::to_string(counts[i]);
    }
    sb += '\n';
    std::cout << sb;
    return 0;
}