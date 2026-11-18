#include <iostream>
#include <string>

bool isValid(const std::string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            bal++;
        } else if (c == ')') {
            if (bal == 0) return false;
            bal--;
        } else {
            return false;
        }
    }
    return bal == 0;
}

int main() {
    int T;
    if (!(std::cin >> T)) return 0;

    std::string s;
    while (T-- > 0 && std::cin >> s) {
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}