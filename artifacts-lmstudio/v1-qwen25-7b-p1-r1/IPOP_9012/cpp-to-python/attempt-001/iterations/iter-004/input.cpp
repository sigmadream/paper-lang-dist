#include <iostream>
#include <stack>
#include <string>
#include <vector>

bool is_valid_parenthesis(const std::string& s) {
    std::stack<char> stack;
    for (char c : s) {
        if (c == '(') {
            stack.push(c);
        } else {
            if (stack.empty()) {
                return false;
            }
            stack.pop();
        }
    }
    return stack.empty();
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);

    int t;
    std::cin >> t;
    std::cin.ignore();

    std::vector<std::string> data(t);
    for (int i = 0; i < t; ++i) {
        std::getline(std::cin, data[i]);
    }

    for (const std::string& s : data) {
        if (is_valid_parenthesis(s)) {
            std::cout << "YES" << std::endl;
        } else {
            std::cout << "NO" << std::endl;
        }
    }

    return 0;
}
