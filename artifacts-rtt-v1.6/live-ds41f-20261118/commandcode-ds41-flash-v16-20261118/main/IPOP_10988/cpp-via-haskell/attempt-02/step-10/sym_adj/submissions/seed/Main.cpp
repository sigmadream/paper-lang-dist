#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::cin >> s;
    std::string t = s;
    std::reverse(t.begin(), t.end());
    std::cout << (s == t ? "1" : "0") << '\n';
    return 0;
}