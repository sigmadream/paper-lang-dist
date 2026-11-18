#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) {
        return 0;
    }

    std::size_t begin = line.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) {
        return 0;
    }
    std::size_t end = line.find_last_not_of(" \t\r\n");
    std::string trimmed = line.substr(begin, end - begin + 1);

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