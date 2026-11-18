#include <iostream>
#include <vector>

long long gcd(long long a, long long b) {
    while (b != 0) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    std::vector<long long> data;
    long long x;
    while (std::cin >> x) {
        data.push_back(x);
    }

    if (data.size() < 2) {
        return 0;
    }

    long long a = data[0];
    long long b = data[1];
    long long g = gcd(a, b);

    std::cout << g << '\n';
    std::cout << (a / g) * b << '\n';

    return 0;
}