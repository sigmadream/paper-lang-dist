#include <iostream>
#include <string>
#include <cctype>

static bool isWhitespace(char c) {
    return std::isspace(static_cast<unsigned char>(c)) != 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string first;
    if (!std::getline(std::cin, first)) return 0;

    int idx = 0;
    int n = static_cast<int>(first.length());
    while (idx < n && isWhitespace(first[idx])) idx++;

    int sign = 1;
    if (idx < n && (first[idx] == '+' || first[idx] == '-')) {
        if (first[idx] == '-') sign = -1;
        idx++;
    }

    int val = 0;
    while (idx < n && std::isdigit(static_cast<unsigned char>(first[idx]))) {
        val = val * 10 + (first[idx] - '0');
        idx++;
    }

    int t = sign * val;
    std::string out;

    for (int i = 0; i < t; i++) {
        bool found = false;
        std::string s;

        while (true) {
            std::string line;
            if (!std::getline(std::cin, line)) break;

            bool empty = true;
            for (char c : line) {
                if (!isWhitespace(c)) {
                    empty = false;
                    break;
                }
            }

            if (!empty) {
                s = line;
                found = true;
                break;
            }
        }

        if (!found) break;

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                balance++;
            } else if (c == ')') {
                balance--;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) {
            valid = false;
        }

        out += valid ? "YES\n" : "NO\n";
    }

    std::cout << out;
    return 0;
}