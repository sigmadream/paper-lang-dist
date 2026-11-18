#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s, t;
    if (std::cin >> s >> t) {
        std::sort(s.begin(), s.end());
        std::sort(t.begin(), t.end());
        std::cout << (s == t ? "1" : "0") << '\n';
    }
    return 0;
}