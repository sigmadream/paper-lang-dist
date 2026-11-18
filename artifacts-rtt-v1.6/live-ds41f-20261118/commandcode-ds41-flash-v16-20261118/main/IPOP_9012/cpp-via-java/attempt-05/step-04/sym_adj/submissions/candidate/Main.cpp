#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // Mimic Java String.trim() for the first line
    auto trim = [](std::string s) {
        size_t start = 0;
        while (start < s.size() && static_cast<unsigned char>(s[start]) <= ' ') ++start;
        size_t end = s.size();
        while (end > start && static_cast<unsigned char>(s[end - 1]) <= ' ') --end;
        return s.substr(start, end - start);
    };

    int t = std::stoi(trim(line));
    std::string output;

    while (t-- > 0) {
        std::string s;
        if (!std::getline(std::cin, s)) s = "";
        s = trim(s);

        int bal = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') ++bal;
            else --bal;

            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) valid = false;

        output += valid ? "YES\n" : "NO\n";
    }

    std::cout << output;
    return 0;
}