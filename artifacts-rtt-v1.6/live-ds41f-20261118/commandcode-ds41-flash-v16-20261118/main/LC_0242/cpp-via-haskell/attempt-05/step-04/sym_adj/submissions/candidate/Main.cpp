#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s, t;
    if (!std::getline(std::cin, s)) return 0;
    if (!std::getline(std::cin, t)) return 0;
    while (!s.empty() && (s.back() == '\r' || s.back() == ' ' || s.back() == '\t')) s.pop_back();
    while (!t.empty() && (t.back() == '\r' || t.back() == ' ' || t.back() == '\t')) t.pop_back();
    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());
    std::cout << (s == t ? "1" : "0") << "\n";
    return 0;
}