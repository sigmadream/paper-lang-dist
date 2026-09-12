#include <iostream>
#include <string>

int main() {
    int n;
    std::cin >> n;

    int count = 0;
    int value = 665;
    while (count < n) {
        ++value;
        if (std::to_string(value).find("666") != std::string::npos) {
            ++count;
        }
    }

    std::cout << value << std::endl;
    return 0;
}
