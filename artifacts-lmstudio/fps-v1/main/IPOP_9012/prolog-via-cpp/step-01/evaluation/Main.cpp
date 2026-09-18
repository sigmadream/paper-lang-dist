#include <iostream>
#include <string>
#include <vector>

bool balanced(const std::string& s) {
    int depth = 0;
    for (char c : s) {
        if (c == '(') {
            depth++;
        } else if (c == ')') {
            if (depth == 0) return false;
            depth--;
        }
    }
    return depth == 0;
}

int main() {
    int T;
    std::cin >> T;
    std::string s;
    for (int i = 0; i < T; ++i) {
        std::cin >> s;
        if (balanced(s)) {
            std::cout << "YES" << std::endl;
        } else {
            std::cout << "NO" << std::endl;
        }
    }
    return 0;
}