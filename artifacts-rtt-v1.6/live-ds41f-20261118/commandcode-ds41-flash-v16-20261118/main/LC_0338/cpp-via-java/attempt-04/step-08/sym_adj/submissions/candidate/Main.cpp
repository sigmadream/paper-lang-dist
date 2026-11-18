#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        return 0;
    }

    const std::string whitespace = " \t\r\n\f\v";
    const std::size_t first = line.find_first_not_of(whitespace);
    if (first == std::string::npos) {
        return 0;
    }
    const std::size_t last = line.find_last_not_of(whitespace);
    const std::string trimmed = line.substr(first, last - first + 1);

    int n = std::stoi(trimmed);

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    for (int i = 0; i <= n; ++i) {
        if (i > 0) {
            std::cout << ' ';
        }
        std::cout << counts[i];
    }
    std::cout << '\n';

    return 0;
}