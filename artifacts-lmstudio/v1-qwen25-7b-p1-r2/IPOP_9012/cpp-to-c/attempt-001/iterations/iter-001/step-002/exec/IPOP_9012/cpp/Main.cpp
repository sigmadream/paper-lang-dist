#include <iostream>
#include <string>

int main() {
    int t;
    std::cin >> t;
    while (t--) {
        std::string s;
        std::cin >> s;
        int bal = 0;
        int valid = 1;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) {
                valid = 0;
                break;
            }
        }
        if (bal != 0) valid = 0;
        if (valid) std::cout << "YES\n";
        else std::cout << "NO\n";
    }
    return 0;
}
