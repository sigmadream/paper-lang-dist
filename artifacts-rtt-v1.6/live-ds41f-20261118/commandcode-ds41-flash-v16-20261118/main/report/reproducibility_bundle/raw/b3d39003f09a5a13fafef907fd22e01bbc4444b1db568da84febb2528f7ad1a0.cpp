#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!(std::cin >> s)) return 0;

    bool palindrome = true;
    for (std::size_t i = 0, j = s.size(); i < j / 2; ++i) {
        if (s[i] != s[j - 1 - i]) {
            palindrome = false;
            break;
        }
    }

    std::cout << (palindrome ? 1 : 0) << '\n';
    return 0;
}