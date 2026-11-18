#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    const std::string whitespace = " \t\r\n";
    const std::size_t first = line.find_first_not_of(whitespace);
    if (first == std::string::npos) return 0;
    const std::size_t last = line.find_last_not_of(whitespace);
    line = line.substr(first, last - first + 1);

    int n = 0;
    try {
        n = std::stoi(line);
    } catch (...) {
        return 0;
    }

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