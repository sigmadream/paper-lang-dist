#include <iostream>
#include <vector>
#include <string>

bool is_valid_parenthesis(const std::string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            bal += 1;
        } else {
            bal -= 1;
        }
        if (bal < 0) {
            return false;
        }
    }
    return bal == 0;
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
