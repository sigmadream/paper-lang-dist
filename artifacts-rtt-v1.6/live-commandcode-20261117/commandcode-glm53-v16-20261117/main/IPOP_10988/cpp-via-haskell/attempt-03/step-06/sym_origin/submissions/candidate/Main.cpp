#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string line;
    std::getline(std::cin, line);
    std::string s;
    for (char c : line) {
        if (c >= 'a' && c <= 'z') s += c;
        else break;
    }
    if (!s.empty()) {
        std::string r = s;
        std::reverse(r.begin(), r.end());
        std::cout << (s == r ? "1" : "0") << "\n";
    }
    return 0;
}