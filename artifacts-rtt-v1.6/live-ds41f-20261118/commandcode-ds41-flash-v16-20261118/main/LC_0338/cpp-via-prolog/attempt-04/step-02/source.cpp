#include <iostream>
#include <string>
#include <sstream>

int countBits(int n) {
    int count = 0;
    while (n > 0) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}

int main() {
    std::string line;
    std::getline(std::cin, line);

    std::string filtered;
    for (char c : line) {
        if (c == '-' || (c >= '0' && c <= '9')) {
            filtered.push_back(c);
        }
    }

    int N = 0;
    if (!filtered.empty()) {
        try {
            N = std::stoi(filtered);
        } catch (...) {
            N = 0;
        }
    }

    std::ostringstream out;
    for (int i = 0; i <= N; ++i) {
        if (i > 0) out << ' ';
        out << countBits(i);
    }

    std::cout << out.str() << '\n';
    return 0;
}