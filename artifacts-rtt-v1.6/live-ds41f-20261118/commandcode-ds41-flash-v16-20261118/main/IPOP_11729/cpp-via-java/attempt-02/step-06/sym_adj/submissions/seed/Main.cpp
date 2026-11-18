#include <iostream>
#include <string>

std::string output;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        output += std::to_string(start);
        output += ' ';
        output += std::to_string(end);
        output += '\n';
        return;
    }

    hanoi(n - 1, start, end, mid);
    output += std::to_string(start);
    output += ' ';
    output += std::to_string(end);
    output += '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    const std::string whitespace = " \t\r\n";
    std::size_t first = line.find_first_not_of(whitespace);
    if (first == std::string::npos) return 0;
    std::size_t last = line.find_last_not_of(whitespace);
    line = line.substr(first, last - first + 1);

    int n = std::stoi(line);
    int count = (1 << n) - 1;

    output.reserve(static_cast<std::size_t>(count) * 5 + 16);
    output += std::to_string(count);
    output += '\n';

    hanoi(n, 1, 2, 3);

    std::cout << output;
    return 0;
}