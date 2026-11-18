#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string line;
    int n = 0;
    if (std::getline(std::cin, line)) {
        size_t pos = line.find_first_not_of(" \t\r\n");
        if (pos != std::string::npos) {
            n = std::stoi(line.substr(pos));
        }
    }
    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }
    for (int i = 0; i <= n; ++i) {
        if (i) std::cout << ' ';
        std::cout << counts[i];
    }
    std::cout << '\n';
    return 0;
}