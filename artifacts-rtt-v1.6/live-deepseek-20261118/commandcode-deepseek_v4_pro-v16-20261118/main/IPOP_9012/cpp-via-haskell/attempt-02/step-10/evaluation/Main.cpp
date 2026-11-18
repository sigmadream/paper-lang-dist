#include <iostream>
#include <string>

bool isBalanced(const std::string& s) {
    int count = 0;
    for (char c : s) {
        if (c == '(') {
            ++count;
        } else if (c == ')') {
            if (count == 0) return false;
            --count;
        } else {
            return false;
        }
    }
    return count == 0;
}

int main() {
    int T;
    if (!(std::cin >> T)) return 0;
    
    for (int i = 0; i < T; ++i) {
        std::string s;
        if (!(std::cin >> s)) break;
        std::cout << (isBalanced(s) ? "YES" : "NO") << '\n';
    }
    
    return 0;
}