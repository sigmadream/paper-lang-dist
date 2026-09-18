#include <iostream>
#include <string>
#include <vector>

bool isBalanced(const std::string& s, int depth = 0) {
    for (char c : s) {
        if (depth < 0) return false;
        if (c == '(') ++depth;
        else --depth;
    }
    return depth == 0;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::string> strings(n);
    for (std::string& s : strings) {
        std::cin >> s;
    }
    for (const std::string& s : strings) {
        if (isBalanced(s)) {
            std::cout << "YES\n";
        } else {
            std::cout << "NO\n";
        }
    }
    return 0;
}