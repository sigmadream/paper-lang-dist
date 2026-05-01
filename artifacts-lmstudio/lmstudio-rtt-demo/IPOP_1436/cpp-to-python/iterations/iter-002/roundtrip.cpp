#include <iostream>
#include <string>

int main() {
    int n;
    std::cin >> n;

    int count = 0;
    int value = 665;
    while (count < n) {
        value += 1;
        std::string str_value = std::to_string(value);
        if (str_value.find("666") != std::string::npos) {
            count += 1;
        }
    }

    std::cout << value << std::endl;

    return 0;
}
