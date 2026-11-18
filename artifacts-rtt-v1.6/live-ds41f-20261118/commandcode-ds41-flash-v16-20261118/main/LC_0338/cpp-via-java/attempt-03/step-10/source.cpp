#include <iostream>
#include <string>
#include <vector>
#include <cctype>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // trim
    std::size_t start = 0, end = line.size();
    while (start < end && std::isspace(static_cast<unsigned char>(line[start]))) ++start;
    while (end > start && std::isspace(static_cast<unsigned char>(line[end - 1]))) --end;
    line = line.substr(start, end - start);
    if (line.empty()) return 0;

    int n = std::stoi(line);

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::ios::sync_with_stdio(false);
    std::string out;
    out.reserve((n + 1) * 7 + 1);
    for (int i = 0; i <= n; ++i) {
        if (i > 0) out += ' ';
        out += std::to_string(counts[i]);
    }
    out += '\n';
    std::cout << out;
    return 0;
}