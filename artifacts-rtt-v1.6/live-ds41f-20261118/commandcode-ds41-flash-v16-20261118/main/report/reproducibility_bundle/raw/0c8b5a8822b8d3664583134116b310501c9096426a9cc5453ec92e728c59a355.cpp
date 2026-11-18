#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::cin.ignore(1000000, '\n');

    for (int i = 0; i < T; ++i) {
        std::string s;
        std::getline(std::cin, s);

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                --balance;
                if (balance < 0) {
                    valid = false;
                    break;
                }
            }
        }

        if (balance != 0) valid = false;

        std::cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}