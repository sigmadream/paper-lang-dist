#include <iostream>
#include <sstream>

void hanoi(int n, int from, int aux, int to, std::ostringstream& out) {
    if (n == 1) {
        out << from << ' ' << to << '\n';
        return;
    }
    hanoi(n - 1, from, to, aux, out);
    out << from << ' ' << to << '\n';
    hanoi(n - 1, aux, from, to, out);
}

int main() {
    int n;
    std::cin >> n;
    if (!std::cin || n < 1 || n > 20) {
        return 0;
    }
    long long moves = (1LL << n) - 1;
    std::ostringstream out;
    out << moves << '\n';
    hanoi(n, 1, 2, 3, out);
    std::cout << out.str();
    return 0;
}