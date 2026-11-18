#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    auto clean = [](std::string& x) {
        x.erase(std::remove_if(x.begin(), x.end(),
                               [](char c) { return c == '\n' || c == '\r'; }),
                x.end());
    };

    clean(s);
    clean(t);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}