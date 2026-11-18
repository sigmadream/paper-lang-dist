#include <iostream>
#include <string>
#include <algorithm>

int main() {
    int T;
    std::cin >> T;
    std::string dummy;
    std::getline(std::cin, dummy); // consume rest of first line

    for (int i = 0; i < T; ++i) {
        std::string line;
        std::getline(std::cin, line);

        int balance = 0;
        int min_balance = 0;

        for (char c : line) {
            if (c == '(') {
                balance++;
            } else if (c == ')') {
                balance--;
            }
            // other characters are ignored (matching Prolog logic)

            if (balance < min_balance) {
                min_balance = balance;
            }
        }

        if (balance == 0 && min_balance >= 0) {
            std::cout << "YES\n";
        } else {
            std::cout << "NO\n";
        }
    }

    return 0;
}