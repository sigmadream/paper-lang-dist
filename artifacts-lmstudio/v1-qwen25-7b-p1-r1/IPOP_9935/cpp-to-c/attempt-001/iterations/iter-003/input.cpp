#include <iostream>
#include <string>

int main() {
    std::string s, bomb;
    std::cin >> s >> bomb;
    
    std::string res = "";
    int b_len = bomb.length();
    
    for (int i = 0; i < s.length(); i++) {
        res += s[i];
        if (res.length() >= b_len) {
            int match = 1;
            for (int j = 0; j < b_len; j++) {
                if (res[res.length() - b_len + j] != bomb[j]) {
                    match = 0;
                    break;
                }
            }
            if (match) {
                res.resize(res.length() - b_len);
            }
        }
    }
    
    if (res.empty()) std::cout << "FRULA\n";
    else std::cout << res << "\n";
    return 0;
}
