#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::getline(std::cin, s);
    std::string t;
    for (char c : s) {
        if (c >= 'a' && c <= 'z') t += c;
        else break;
    }
    std::string r = t;
    std::reverse(r.begin(), r.end());
    std::cout << (t == r ? "1" : "0") << "\n";
    return 0;
}