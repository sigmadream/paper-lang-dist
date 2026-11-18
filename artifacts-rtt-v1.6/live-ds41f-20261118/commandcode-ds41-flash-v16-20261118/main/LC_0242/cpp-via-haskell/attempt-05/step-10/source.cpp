#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

static bool isCWhitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' ||
           c == '\v' || c == '\f' || c == '\r';
}

static std::string stripTrailing(std::string s) {
    while (!s.empty() && isCWhitespace(s.back())) {
        s.pop_back();
    }
    return s;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(std::cin, line)) {
        lines.push_back(line);
    }

    if (lines.empty()) {
        return 0;
    }

    if (lines.size() == 1) {
        std::cout << "0\n";
        return 0;
    }

    std::string s = stripTrailing(lines[0]);
    std::string t = stripTrailing(lines[1]);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? "1\n" : "0\n");
    return 0;
}