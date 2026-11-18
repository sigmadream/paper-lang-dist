#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    if (!(std::cin >> s)) return 0;

    std::string t = s;
    std::reverse(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}