#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::getline(std::cin, s);
    s.erase(std::remove(s.begin(), s.end(), '\r'), s.end());
    std::string r(s.rbegin(), s.rend());
    std::cout << (s == r ? "1" : "0") << std::endl;
    return 0;
}