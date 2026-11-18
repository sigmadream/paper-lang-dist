#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    s.erase(std::remove(s.begin(), s.end(), '\r'), s.end());
    t.erase(std::remove(t.begin(), t.end(), '\r'), t.end());

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}