#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string input;
    std::cin >> input;
    std::string reversed_input = input;
    std::reverse(reversed_input.begin(), reversed_input.end());
    if (input == reversed_input) {
        std::cout << "1" << std::endl;
    } else {
        std::cout << "0" << std::endl;
    }
    return 0;
}