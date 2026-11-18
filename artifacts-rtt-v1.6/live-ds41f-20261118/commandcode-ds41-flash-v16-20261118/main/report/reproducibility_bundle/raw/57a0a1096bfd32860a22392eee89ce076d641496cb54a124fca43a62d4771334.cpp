#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    if (!(std::cin >> t)) return 0;

    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!(std::cin >> s)) break;

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else {
                --balance;
            }

            if (balance < 0) {
                valid = false;
            }
        }

        if (balance != 0) {
            valid = false;
        }

        std::cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}