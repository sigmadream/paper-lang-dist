#include <iostream>
#include <vector>
#include <string>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // trim
    size_t start = line.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return 0;
    size_t end = line.find_last_not_of(" \t\r\n");
    line = line.substr(start, end - start + 1);

    int n = std::stoi(line);

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::string out;
    for (int i = 0; i <= n; ++i) {
        if (i > 0) out += ' ';
        out += std::to_string(counts[i]);
    }
    out += '\n';

    std::cout << out;
    return 0;
}