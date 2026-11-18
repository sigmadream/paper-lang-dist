#include <algorithm>
#include <iostream>
#include <string>

int main() {
    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    auto strip_cr = [](std::string& str) {
        if (!str.empty() && str.back() == '\r') str.pop_back();
    };
    strip_cr(s);
    strip_cr(t);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}