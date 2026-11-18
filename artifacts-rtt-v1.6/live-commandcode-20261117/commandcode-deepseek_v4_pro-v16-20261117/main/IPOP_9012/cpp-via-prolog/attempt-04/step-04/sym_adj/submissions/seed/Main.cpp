#include <iostream>
#include <string>
#include <limits>

int main() {
    int T;
    std::cin >> T;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    for (int i = 0; i < T; ++i) {
        std::string s;
        std::getline(std::cin, s);

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