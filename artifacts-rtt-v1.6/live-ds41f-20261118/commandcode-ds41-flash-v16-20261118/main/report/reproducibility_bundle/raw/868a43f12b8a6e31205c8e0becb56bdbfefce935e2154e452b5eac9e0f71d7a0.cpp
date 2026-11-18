#include <iostream>
#include <optional>
#include <string>

std::optional<long long> read_nat() {
    char c;
    while (std::cin.get(c)) {
        if (c >= '0' && c <= '9') {
            std::string s;
            s.push_back(c);
            while (std::cin.get(c)) {
                if (c >= '0' && c <= '9') {
                    s.push_back(c);
                } else {
                    break;
                }
            }
            return std::stoll(s);
        }
    }
    return std::nullopt;
}

long long gcd_ll(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    auto a = read_nat();
    if (!a) return 0;

    auto b = read_nat();
    if (!b) return 0;

    long long g = gcd_ll(*a, *b);
    long long l = (*a / g) * (*b);

    std::cout << g << "\n" << l << "\n";
    return 0;
}