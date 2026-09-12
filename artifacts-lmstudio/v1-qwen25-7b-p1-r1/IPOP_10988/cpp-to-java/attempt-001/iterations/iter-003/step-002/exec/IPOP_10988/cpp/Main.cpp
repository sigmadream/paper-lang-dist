#include <iostream>
#include <string>

int main() {
    std::string s;
    std::cin >> s;
    
    bool valid = true;
    for (int i = 0; i < s.length() / 2; i++) {
        if (s[i] != s[s.length() - 1 - i]) {
            valid = false;
            break;
        }
    }
    std::cout << (valid ? 1 : 0) << std::endl;
    return 0;
}
