#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    auto remove_cr = [](std::string &str) {
        str.erase(std::remove(str.begin(), str.end(), '\r'), str.end());
    };

    remove_cr(s);
    remove_cr(t);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}