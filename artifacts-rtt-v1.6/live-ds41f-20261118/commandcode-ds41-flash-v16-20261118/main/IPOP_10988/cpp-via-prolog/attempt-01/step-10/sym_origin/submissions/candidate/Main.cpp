#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    if (std::cin >> s) {
        std::string reversed = s;
        std::reverse(reversed.begin(), reversed.end());
        std::cout << (s == reversed ? 1 : 0) << '\n';
    }
    return 0;
}