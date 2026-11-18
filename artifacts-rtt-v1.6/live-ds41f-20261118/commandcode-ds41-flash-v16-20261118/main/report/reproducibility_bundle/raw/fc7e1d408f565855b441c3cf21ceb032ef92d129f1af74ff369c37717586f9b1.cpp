#include <iostream>
#include <string>
#include <vector>
#include <cctype>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    std::size_t start = 0;
    while (start < line.size() && std::isspace(static_cast<unsigned char>(line[start]))) ++start;
    std::size_t end = line.size();
    while (end > start && std::isspace(static_cast<unsigned char>(line[end - 1]))) --end;

    if (start == end) return 0;

    std::string trimmed = line.substr(start, end - start);
    int n = 0;
    try {
        std::size_t pos = 0;
        n = std::stoi(trimmed, &pos);
        if (pos != trimmed.size()) return 0;
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