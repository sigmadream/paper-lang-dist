#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) {
        return 0;
    }
    s.erase(std::remove(s.begin(), s.end(), '\r'), s.end());
    std::string r = s;
    std::reverse(r.begin(), r.end());
    std::cout << (s == r ? 1 : 0) << '\n';
    return 0;
}