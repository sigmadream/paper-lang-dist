#include <iostream>
#include <string>

int main() {
    std::string s;
    std::getline(std::cin, s);

    if (!s.empty() && s.back() == '\r') {
        s.pop_back();
    }

    bool palindrome = true;
    int left = 0;
    int right = static_cast<int>(s.size()) - 1;

    while (left < right) {
        if (s[left] != s[right]) {
            palindrome = false;
            break;
        }
        ++left;
        --right;
    }

    std::cout << (palindrome ? 1 : 0) << '\n';
    return 0;
}