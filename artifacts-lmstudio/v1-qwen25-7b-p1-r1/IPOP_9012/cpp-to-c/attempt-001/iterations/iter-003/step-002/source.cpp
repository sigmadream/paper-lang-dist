#include <iostream>
#include <string>

int main() {
    int t;
    std::cin >> t;
    while (t--) {
        std::string s;
        std::cin >> s;
        int bal = 0;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) {
                std::cout << "NO\n";
                goto next;
            }
        }
        if (bal != 0) {
            std::cout << "NO\n";
        } else {
            std::cout << "YES\n";
        }
        next:;
    }
    return 0;
}
