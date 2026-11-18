#include <iostream>
#include <string>
#include <limits>

int main() {
    int T;
    std::cin >> T;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    for (int i = 0; i < T; ++i) {
        std::string line;
        std::getline(std::cin, line);

        int balance = 0;
        bool valid = true;

        for (char c : line) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance == 0) {
                    valid = false;
                    break;
                }
                --balance;
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