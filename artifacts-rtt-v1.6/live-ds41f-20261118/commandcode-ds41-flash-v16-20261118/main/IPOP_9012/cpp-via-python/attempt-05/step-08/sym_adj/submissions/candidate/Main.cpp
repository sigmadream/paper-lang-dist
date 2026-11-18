#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    if (!(std::cin >> t)) return 0;

    while (t--) {
        std::string s;
        std::cin >> s;

        int balance = 0;
        bool valid = true;

        for (char ch : s) {
            if (ch == '(') {
                ++balance;
            } else {
                --balance;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) valid = false;

        std::cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}