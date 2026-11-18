#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::cin.ignore(1000000, '\n');

    for (int i = 0; i < T; ++i) {
        std::string line;
        if (!std::getline(std::cin, line)) break;

        bool ok = true;
        int balance = 0;

        for (char c : line) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance == 0) {
                    ok = false;
                    break;
                }
                --balance;
            }
        }

        if (balance != 0) ok = false;

        std::cout << (ok ? "YES\n" : "NO\n");
    }

    return 0;
}