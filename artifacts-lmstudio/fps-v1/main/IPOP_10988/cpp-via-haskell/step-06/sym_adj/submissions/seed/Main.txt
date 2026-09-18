#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string input;
    std::cin >> input;
    std::string reversedInput = input;
    std::reverse(reversedInput.begin(), reversedInput.end());
    if (input == reversedInput) {
        std::cout << "1" << std::endl;
    } else {
        std::cout << "0" << std::endl;
    }
    return 0;
}