#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!std::getline(std::cin, first)) {
        return 0;
    }

    auto trim = [](const std::string& str) {
        std::size_t start = 0;
        std::size_t end = str.size();

        while (start < end &&
               (str[start] == ' ' || str[start] == '\t' ||
                str[start] == '\r' || str[start] == '\n')) {
            ++start;
        }

        while (end > start &&
               (str[end - 1] == ' ' || str[end - 1] == '\t' ||
                str[end - 1] == '\r' || str[end - 1] == '\n')) {
            --end;
        }

        if (start < end) {
            return str.substr(start, end - start);
        }
        return std::string();
    };

    int t = std::stoi(trim(first));
    std::string output;

    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!std::getline(std::cin, s)) {
            break;
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