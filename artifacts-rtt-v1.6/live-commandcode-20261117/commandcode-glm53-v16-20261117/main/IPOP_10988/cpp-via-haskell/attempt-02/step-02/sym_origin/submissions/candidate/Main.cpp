#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::cin >> s;
    std::string r(s.rbegin(), s.rend());
    std::cout << (s == r ? 1 : 0) << "\n";
    return 0;
}