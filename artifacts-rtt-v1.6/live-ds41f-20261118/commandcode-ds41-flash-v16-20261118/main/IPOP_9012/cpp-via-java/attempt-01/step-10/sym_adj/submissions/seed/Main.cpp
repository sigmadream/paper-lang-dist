#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!std::getline(std::cin, first)) {
        return 0;
    }

    int t = std::stoi(first);
    std::string output;

    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!std::getline(std::cin, s)) {
            break;
        }

        // trim
        size_t start = s.find_first_not_of(" \t\r\n");
        if (start == std::string::npos) {
            s.clear();
        } else {
            size_t end = s.find_last_not_of(" \t\r\n");
            s = s.substr(start, end - start + 1);
        }

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