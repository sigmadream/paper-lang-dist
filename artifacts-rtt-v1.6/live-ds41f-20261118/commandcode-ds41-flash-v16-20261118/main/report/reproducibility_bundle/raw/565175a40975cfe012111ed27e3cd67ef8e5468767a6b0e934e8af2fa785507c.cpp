#include <iostream>
#include <string>
#include <cctype>

static std::string trim(const std::string& s) {
    size_t begin = 0;
    size_t end = s.size();

    while (begin < end && std::isspace(static_cast<unsigned char>(s[begin]))) {
        ++begin;
    }
    while (end > begin && std::isspace(static_cast<unsigned char>(s[end - 1]))) {
        --end;
    }

    return s.substr(begin, end - begin);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) {
        return 0;
    }

    std::string line;
    std::getline(std::cin, line);

    for (int i = 0; i < T; ++i) {
        if (!std::getline(std::cin, line)) {
            break;
        }

        line = trim(line);

        int balance = 0;
        bool ok = true;

        for (char c : line) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance > 0) {
                    --balance;
                } else {
                    ok = false;
                    break;
                }
            }
        }

        if (balance != 0) {
            ok = false;
        }

        std::cout << (ok ? "YES" : "NO") << '\n';
    }

    return 0;
}