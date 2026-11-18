#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::string dummy;
    std::getline(std::cin, dummy);

    for (int i = 0; i < T; ++i) {
        std::string line;
        if (!std::getline(std::cin, line)) break;

        int left = 0;
        int right = static_cast<int>(line.size()) - 1;

        while (left < static_cast<int>(line.size()) &&
               std::isspace(static_cast<unsigned char>(line[left]))) {
            ++left;
        }
        while (right >= 0 &&
               std::isspace(static_cast<unsigned char>(line[right]))) {
            --right;
        }

        bool ok = true;

        if (left > right) {
            ok = false;
        } else {
            int balance = 0;

            for (int j = left; j <= right; ++j) {
                char c = line[j];

                if (std::isspace(static_cast<unsigned char>(c))) {
                    ok = false;
                    break;
                }

                if (c == '(') {
                    ++balance;
                } else if (c == ')') {
                    if (balance <= 0) {
                        ok = false;
                        break;
                    }
                    --balance;
                } else {
                    ok = false;
                    break;
                }
            }

            if (balance != 0) ok = false;
        }

        std::cout << (ok ? "YES" : "NO") << '\n';
    }

    return 0;
}