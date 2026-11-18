#include <iostream>
#include <vector>
#include <sstream>

int main() {
    std::ios::sync_with_stdio(false);
    int n;
    if (!(std::cin >> n)) return 0;
    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) counts[i] = counts[i / 2] + i % 2;
    std::ostringstream oss;
    for (int i = 0; i <= n; ++i) {
        if (i > 0) oss << ' ';
        oss << counts[i];
    }
    oss << '\n';
    std::cout << oss.str();
    return 0;
}