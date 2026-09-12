#include <iostream>
#include <string>

int main() {
    int t;
    std::cin >> t;
    std::cin.ignore();
    while (t-- > 0) {
        std::string s;
        std::getline(std::cin, s);
        int bal = 0;
        bool valid = true;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) {
                valid = false;
                break;
            }
        }
        if (bal != 0) valid = false;
        std::cout << (valid ? "YES" : "NO") << std::endl;
    }
    return 0;
}
