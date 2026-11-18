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

        if (valid && balance == 0) {
            std::cout << "YES\n";
        } else {
            std::cout << "NO\n";
        }
    }

    return 0;
}