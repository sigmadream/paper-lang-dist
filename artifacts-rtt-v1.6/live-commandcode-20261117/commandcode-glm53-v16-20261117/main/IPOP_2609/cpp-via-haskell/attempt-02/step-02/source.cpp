#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string contents, tmp;
    std::getline(std::cin, contents);
    std::istringstream iss(contents);
    long long a, b;
    if (iss >> a >> b) {
        long long x = a, y = b;
        while (y != 0) { long long r = x % y; x = y; y = r; }
        long long g = x;
        std::cout << g << "\n" << (a / g) * b << "\n";
    }
    return 0;
}