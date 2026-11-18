#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) return 0;

    if (!s.empty() && s.back() == '\r') {
        s.pop_back();
    }

    std::string rev = s;
    std::reverse(rev.begin(), rev.end());

    std::cout << (s == rev ? 1 : 0) << '\n';
    return 0;
}