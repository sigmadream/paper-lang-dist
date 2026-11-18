#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s, t;
    if (!std::getline(std::cin, s)) s = "";
    if (!std::getline(std::cin, t)) t = "";

    auto clean = [](const std::string& str) {
        std::string result;
        result.reserve(str.size());
        for (char c : str) {
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') continue;
            result.push_back(c);
        }
        return result;
    };

    std::string a = clean(s);
    std::string b = clean(t);

    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());

    std::cout << (a == b ? 1 : 0) << '\n';
    return 0;
}