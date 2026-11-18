#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::getline(std::cin, s);
    std::string r = s;
    std::reverse(r.begin(), r.end());
    std::cout << (s == r ? "1" : "0") << "\n";
    return 0;
}