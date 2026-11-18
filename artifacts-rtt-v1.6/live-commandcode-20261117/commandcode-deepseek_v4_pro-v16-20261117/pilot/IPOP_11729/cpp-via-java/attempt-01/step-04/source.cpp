#include <iostream>
#include <string>

void hanoi(int n, int from, int aux, int to, std::string& out) {
    if (n == 1) {
        out += std::to_string(from) + " " + std::to_string(to) + "\n";
        return;
    }
    hanoi(n - 1, from, to, aux, out);
    out += std::to_string(from) + " " + std::to_string(to) + "\n";
    hanoi(n - 1, aux, from, to, out);
}

int main() {
    int n;
    if (!(std::cin >> n)) {
        return 0;
    }
    if (n < 1 || n > 20) {
        return 0;
    }
    long long count = (1LL << n) - 1;
    std::string output;
    output += std::to_string(count) + "\n";
    hanoi(n, 1, 2, 3, output);
    std::cout << output;
    return 0;
}