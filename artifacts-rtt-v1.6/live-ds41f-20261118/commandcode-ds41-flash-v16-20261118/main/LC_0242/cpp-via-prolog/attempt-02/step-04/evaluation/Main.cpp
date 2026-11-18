#include <iostream>
#include <string>
#include <algorithm>

std::string readLine() {
    std::string s;
    if (!std::getline(std::cin, s)) return "";
    return s;
}

std::string removeWhitespace(const std::string& s) {
    std::string result;
    for (char c : s) {
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') continue;
        result.push_back(c);
    }
    return result;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s = readLine();
    std::string t = readLine();

    s = removeWhitespace(s);
    t = removeWhitespace(t);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}