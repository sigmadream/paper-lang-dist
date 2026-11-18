#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::getline(std::cin, s);
    if (!s.empty() && s.back() == '\r') s.pop_back();
    bool valid = true;
    for (size_t i = 0; i < s.size() / 2; i++) {
        if (s[i] != s[s.size() - 1 - i]) {
            valid = false;
            break;
        }
    }
    std::cout << (valid ? 1 : 0) << std::endl;
    return 0;
}