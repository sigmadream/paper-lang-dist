#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    while (T--) {
        std::string s;
        std::cin >> s;

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            balance += (c == '(') ? 1 : -1;
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