#include <iostream>
#include <string>

int main() {
    std::string s, bomb;
    std::cin >> s >> bomb;
    
    std::string res;
    int b_len = bomb.length();
    
    for (char c : s) {
        res += c;
        if (res.length() >= b_len) {
            bool match = true;
            for (int i = 0; i < b_len; i++) {
                if (res[res.length() - b_len + i] != bomb[i]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                res.resize(res.length() - b_len);
            }
        }
    }
    
    if (res.empty()) std::cout << "FRULA";
    else std::cout << res;
    
    return 0;
}
