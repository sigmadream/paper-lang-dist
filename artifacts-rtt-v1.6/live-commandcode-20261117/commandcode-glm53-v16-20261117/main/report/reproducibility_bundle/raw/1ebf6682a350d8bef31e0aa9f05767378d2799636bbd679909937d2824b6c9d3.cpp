#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::string s;
        for (char c : line) {
            if (c >= 'a' && c <= 'z') s += c;
            else break;
        }
        if (s.empty()) continue;
        std::string r(s.rbegin(), s.rend());
        std::cout << (s == r ? "1" : "0") << "\n";
    }
    return 0;
}