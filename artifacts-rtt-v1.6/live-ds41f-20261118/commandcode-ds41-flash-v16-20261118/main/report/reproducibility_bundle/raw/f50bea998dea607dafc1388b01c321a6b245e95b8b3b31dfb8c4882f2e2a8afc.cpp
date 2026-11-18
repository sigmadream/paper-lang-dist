#include <iostream>
#include <string>
#include <vector>
#include <cctype>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    std::size_t begin = 0;
    while (begin < line.size() && std::isspace(static_cast<unsigned char>(line[begin]))) {
        ++begin;
    }

    std::size_t end = line.size();
    while (end > begin && std::isspace(static_cast<unsigned char>(line[end - 1]))) {
        --end;
    }

    if (begin == end) return 0;

    int n = std::stoi(line.substr(begin, end - begin));

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }

    std::string output;
    output.reserve(static_cast<std::size_t>(n + 1) * 3);

    for (int i = 0; i <= n; ++i) {
        if (i > 0) output.push_back(' ');
        output += std::to_string(counts[i]);
    }
    output.push_back('\n');

    std::cout << output;
    return 0;
}