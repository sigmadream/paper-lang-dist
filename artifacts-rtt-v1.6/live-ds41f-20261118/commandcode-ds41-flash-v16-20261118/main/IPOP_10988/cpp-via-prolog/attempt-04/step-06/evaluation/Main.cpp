#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) {
        return 0;
    }
    while (!s.empty() && (s.back() == '\r' || s.back() == '\n')) {
        s.pop_back();
    }
    std::string reversed(s.rbegin(), s.rend());
    std::cout << (s == reversed ? 1 : 0) << '\n';
    return 0;
}