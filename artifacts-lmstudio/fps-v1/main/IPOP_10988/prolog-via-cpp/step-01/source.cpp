#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string word;
    std::cin >> word;
    std::string reversed_word = word;
    std::reverse(reversed_word.begin(), reversed_word.end());
    if (word == reversed_word) {
        std::cout << 1 << std::endl;
    } else {
        std::cout << 0 << std::endl;
    }
    return 0;
}