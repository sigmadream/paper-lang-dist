#include <iostream>
#include <string>

int main() {
    int T;
    std::cin >> T;
    std::cin.ignore(); // discard newline after T

    for (int i = 0; i < T; ++i) {
        std::string s;
        std::getline(std::cin, s);

        int balance = 0;
        bool valid = true;
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

        if (valid && balance == 0) {
            std::cout << "YES\n";
        } else {
            std::cout << "NO\n";
        }
    }

    return 0;
}