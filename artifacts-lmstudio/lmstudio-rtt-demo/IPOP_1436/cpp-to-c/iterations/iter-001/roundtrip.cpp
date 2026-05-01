#include <iostream>
#include <string>

int main() {
    int n;
    std::cin >> n;

    int count = 0;
    int value = 665;
    while (count < n) {
        ++value;
        std::string str = std::to_string(value);
        if (str.find("666") != std::string::npos) {
            ++count;
        }
    }

    std::cout << value << std::endl;
    return 0;
}
