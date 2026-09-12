#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string s, bomb;
    std::cin >> s >> bomb;

    std::vector<char> res;
    int b_len = bomb.length();

    for (char c : s) {
        res.push_back(c);
        if (res.size() >= b_len) {
            bool match = true;
            for (int i = 0; i < b_len; ++i) {
                if (res[res.size() - b_len + i] != bomb[i]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                res.resize(res.size() - b_len);
            }
        }
    }

    if (res.empty()) {
        std::cout << "FRULA" << std::endl;
    } else {
        for (char c : res) {
            std::cout << c;
        }
        std::cout << std::endl;
    }

    return 0;
}
