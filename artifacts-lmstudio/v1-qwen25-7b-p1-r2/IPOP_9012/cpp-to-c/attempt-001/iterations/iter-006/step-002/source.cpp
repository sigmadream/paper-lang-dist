#include <iostream>
#include <string>

int main() {
    int t;
    std::cin >> t;
    while (t--) {
        std::string s;
        std::cin >> s;
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
        if (valid) std::cout << "YES\n";
        else std::cout << "NO\n";
    }
    return 0;
}
