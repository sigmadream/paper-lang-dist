#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s;
    if (std::cin >> s) {
        std::string r = s;
        std::reverse(r.begin(), r.end());
        if (s == r) {
            std::cout << "1\n";
        } else {
            std::cout << "0\n";
        }
    }
    return 0;
}