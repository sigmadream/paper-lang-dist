#include <iostream>
#include <string>
#include <algorithm>
#include <unordered_map>

int main() {
    std::string s, t;
    std::cin >> s >> t;

    std::unordered_map<char, int> freq_s, freq_t;

    for (char c : s) {
        freq_s[c]++;
    }

    for (char c : t) {
        freq_t[c]++;
    }

    if (freq_s == freq_t) {
        std::cout << 1 << std::endl;
    } else {
        std::cout << 0 << std::endl;
    }

    return 0;
}