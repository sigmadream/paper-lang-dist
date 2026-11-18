#include <iostream>
#include <string>
#include <sstream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) {
        return 0;
    }

    std::istringstream iss(line);
    std::string token;
    if (!(iss >> token)) {
        return 0;
    }

    int n;
    try {
        std::size_t pos = 0;
        n = std::stoi(token, &pos);
        if (pos != token.size()) {
            return 0;
        }
    } catch (...) {
        return 0;
    }

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