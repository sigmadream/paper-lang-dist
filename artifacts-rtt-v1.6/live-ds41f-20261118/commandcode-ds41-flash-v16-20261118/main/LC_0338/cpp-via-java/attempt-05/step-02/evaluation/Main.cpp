#include <iostream>
#include <string>
#include <sstream>
#include <vector>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;
    // trim
    size_t start = line.find_first_not_of(" \t\r\n");
    size_t end = line.find_last_not_of(" \t\r\n");
    if (start == std::string::npos) return 0;
    line = line.substr(start, end - start + 1);

    int n = std::stoi(line);
    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        counts[i] = counts[i / 2] + (i % 2);
    }
    std::string out;
    for (size_t i = 0; i < counts.size(); i++) {
        if (i > 0) out += ' ';
        out += std::to_string(counts[i]);
    }
    out += '\n';
    std::cout << out;
    return 0;
}