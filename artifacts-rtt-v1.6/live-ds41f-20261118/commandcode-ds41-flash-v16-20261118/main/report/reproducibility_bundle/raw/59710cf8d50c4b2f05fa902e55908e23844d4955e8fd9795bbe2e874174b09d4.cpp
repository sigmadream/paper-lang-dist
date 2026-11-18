#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!(std::cin >> s)) return 0;
    bool valid = true;
    for (int i = 0; i < static_cast<int>(s.size()) / 2; i++) {
        if (s[i] != s[s.size() - 1 - i]) {
            valid = false;
            break;
        }
    }
    std::cout << (valid ? 1 : 0) << std::endl;
    return 0;
}