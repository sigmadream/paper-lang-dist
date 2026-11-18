#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) {
        return 0;
    }

    int left = 0;
    int right = static_cast<int>(s.size()) - 1;
    while (left <= right && static_cast<unsigned char>(s[left]) <= ' ') {
        ++left;
    }
    while (right >= left && static_cast<unsigned char>(s[right]) <= ' ') {
        --right;
    }

    if (left > right) {
        return 0;
    }

    bool valid = true;
    int n = right - left + 1;
    for (int i = 0; i < n / 2; ++i) {
        if (s[left + i] != s[right - i]) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}