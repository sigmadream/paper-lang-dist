#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string input;
    std::getline(std::cin, input);

    std::string s = input.substr(0, input.find(' '));
    std::string reversed = s;
    std::reverse(reversed.begin(), reversed.end());

    std::cout << (s == reversed ? "1" : "0") << '\n';
    return 0;
}