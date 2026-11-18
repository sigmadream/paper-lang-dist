#include <iostream>
#include <string>
#include <sstream>
#include <vector>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // trim
    size_t start = line.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return 0;
    size_t end = line.find_last_not_of(" \t\r\n");
    std::string trimmed = line.substr(start, end - start + 1);
    if (trimmed.empty()) return 0;

    int n;
    try {
        size_t pos = 0;
        n = std::stoi(trimmed, &pos);
        if (pos != trimmed.size()) return 0;
    } catch (...) {
        return 0;
    }

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::ostringstream sb;
    for (int i = 0; i <= n; i++) {
        if (i > 0) sb << ' ';
        sb << counts[i];
    }
    sb << '\n';

    std::cout << sb.str();
    return 0;
}