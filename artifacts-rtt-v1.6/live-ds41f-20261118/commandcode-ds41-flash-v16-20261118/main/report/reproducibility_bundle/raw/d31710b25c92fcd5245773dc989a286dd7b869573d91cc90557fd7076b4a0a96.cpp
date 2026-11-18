#include <iostream>
#include <string>
#include <cctype>
#include <limits>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    for (int tc = 0; tc < T; ++tc) {
        std::string line;
        if (!std::getline(std::cin, line)) break;

        size_t start = 0;
        while (start < line.size() && std::isspace(static_cast<unsigned char>(line[start]))) {
            ++start;
        }

        size_t end = line.size();
        while (end > start && std::isspace(static_cast<unsigned char>(line[end - 1]))) {
            --end;
        }

        std::string s = line.substr(start, end - start);

        bool valid = !s.empty();
        int balance = 0;

        if (valid) {
            for (char c : s) {
                if (c == '(') {
                    ++balance;
                } else if (c == ')') {
                    if (balance == 0) {
                        valid = false;
                        break;
                    }
                    --balance;
                } else {
                    valid = false;
                    break;
                }
            }

            if (balance != 0) valid = false;
        }

        std::cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}