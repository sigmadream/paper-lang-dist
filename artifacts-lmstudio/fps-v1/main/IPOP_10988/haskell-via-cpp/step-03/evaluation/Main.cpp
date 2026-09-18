#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::cin >> s;
    if (s == std::string(s.rbegin(), s.rend())) {
        std::cout << "1" << std::endl;
    } else {
        std::cout << "0" << std::endl;
    }
    return 0;
}