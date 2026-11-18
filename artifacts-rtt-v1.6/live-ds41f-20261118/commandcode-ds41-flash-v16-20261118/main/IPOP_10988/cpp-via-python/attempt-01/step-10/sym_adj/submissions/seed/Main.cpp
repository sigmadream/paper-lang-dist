#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!(std::cin >> s)) {
        return 0;
    }

    int n = static_cast<int>(s.size());
    bool palindrome = true;
    for (int i = 0; i < n / 2; ++i) {
        if (s[i] != s[n - 1 - i]) {
            palindrome = false;
            break;
        }
    }

    std::cout << (palindrome ? 1 : 0) << '\n';
    return 0;
}