#include <iostream>
#include <string>
#include <sstream>

int gcd(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) return 0;
    std::istringstream iss(line);
    long long a, b;
    if (iss >> a >> b) {
        long long g = gcd(a, b);
        std::cout << g << "\n";
        std::cout << (a / g) * b << "\n";
    }
    return 0;
}