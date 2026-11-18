#include <algorithm>
#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    std::getline(std::cin, s);
    std::getline(std::cin, t);

    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!t.empty() && t.back() == '\r') t.pop_back();

    std::string ss = s;
    std::string tt = t;
    std::sort(ss.begin(), ss.end());
    std::sort(tt.begin(), tt.end());

    std::cout << (ss == tt ? 1 : 0) << '\n';
    return 0;
}