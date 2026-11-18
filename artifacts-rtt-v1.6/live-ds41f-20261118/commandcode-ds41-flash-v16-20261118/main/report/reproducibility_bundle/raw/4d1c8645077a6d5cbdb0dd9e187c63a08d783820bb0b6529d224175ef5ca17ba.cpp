#include <iostream>
#include <string>

static std::string trim(const std::string& s) {
    std::size_t start = 0;
    while (start < s.size() && s[start] <= ' ') {
        ++start;
    }
    std::size_t end = s.size();
    while (end > start && s[end - 1] <= ' ') {
        --end;
    }
    return s.substr(start, end - start);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!std::getline(std::cin, first)) {
        return 0;
    }

    int t = std::stoi(trim(first));
    std::string output;

    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!std::getline(std::cin, s)) {
            s = "";
        }
        s = trim(s);

        int bal = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++bal;
            } else {
                --bal;
            }
            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) {
            valid = false;
        }

        output += valid ? "YES\n" : "NO\n";
    }

    std::cout << output;
    return 0;
}