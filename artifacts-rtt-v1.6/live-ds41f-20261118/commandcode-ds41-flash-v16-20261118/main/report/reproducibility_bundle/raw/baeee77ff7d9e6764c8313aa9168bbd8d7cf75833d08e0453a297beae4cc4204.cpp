#include <iostream>
#include <string>
#include <cctype>

static int count_bits(int n) {
    int c = 0;
    while (n > 0) {
        c += n & 1;
        n >>= 1;
    }
    return c;
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        return 0;
    }

    std::string digits;
    for (char ch : line) {
        unsigned char uc = static_cast<unsigned char>(ch);
        if (uc == 32 || uc == 9 || uc == 13 || uc == 10) {
            continue;
        }
        digits.push_back(ch);
    }

    if (digits.empty()) {
        return 0;
    }

    int N = std::stoi(digits);

    std::cout << 0;
    for (int i = 1; i <= N; ++i) {
        std::cout << ' ' << count_bits(i);
    }
    std::cout << '\n';

    return 0;
}