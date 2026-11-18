#include <iostream>
#include <string>
#include <vector>

bool isBalanced(const std::string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance == 0) return false;
            --balance;
        }
    }
    return balance == 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::vector<std::string> strings(T);
    for (int i = 0; i < T; ++i) {
        std::cin >> strings[i];
    }

    for (const auto& s : strings) {
        std::cout << (isBalanced(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}