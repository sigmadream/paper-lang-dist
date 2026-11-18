#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!(std::cin >> s)) return 0;

    std::string reversed(s.rbegin(), s.rend());
    std::cout << (s == reversed ? 1 : 0) << '\n';
    return 0;
}