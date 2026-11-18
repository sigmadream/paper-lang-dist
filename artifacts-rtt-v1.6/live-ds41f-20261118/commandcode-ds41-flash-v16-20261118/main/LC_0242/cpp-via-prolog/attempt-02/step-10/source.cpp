#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

static std::string filterWs(const std::string& s) {
    std::string r;
    r.reserve(s.size());
    for (char c : s) {
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') continue;
        r.push_back(c);
    }
    return r;
}

int main() {
    std::string s, t;
    if (!std::getline(std::cin, s)) s = "";
    if (!std::getline(std::cin, t)) t = "";

    std::string a = filterWs(s);
    std::string b = filterWs(t);

    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());

    std::cout << (a == b ? 1 : 0) << "\n";
    return 0;
}