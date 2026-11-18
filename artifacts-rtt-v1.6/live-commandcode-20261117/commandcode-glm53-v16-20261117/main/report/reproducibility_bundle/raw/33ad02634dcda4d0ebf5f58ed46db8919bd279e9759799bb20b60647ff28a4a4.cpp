#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::getline(std::cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    std::string r(s.rbegin(), s.rend());
    std::cout << (s == r ? 1 : 0) << "\n";
    return 0;
}