#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

static std::string stripTrailing(const std::string& s) {
    std::size_t end = s.size();
    while (end > 0 && std::isspace(static_cast<unsigned char>(s[end - 1]))) {
        --end;
    }
    return s.substr(0, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(std::cin, line)) {
        lines.push_back(line);
    }

    if (lines.size() >= 2) {
        std::string s = stripTrailing(lines[0]);
        std::string t = stripTrailing(lines[1]);

        std::sort(s.begin(), s.end());
        std::sort(t.begin(), t.end());

        std::cout << (s == t ? "1\n" : "0\n");
    } else if (lines.size() == 1) {
        std::cout << "0\n";
    }

    return 0;
}