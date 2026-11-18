#include <iostream>
#include <sstream>

void hanoi(int n, int start, int mid, int end, std::ostringstream& out) {
    if (n == 1) {
        out << start << ' ' << end << '\n';
        return;
    }
    hanoi(n - 1, start, end, mid, out);
    out << start << ' ' << end << '\n';
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    int n;
    std::cin >> n;

    int moves = (1 << n) - 1;
    std::ostringstream out;
    out << moves << '\n';
    hanoi(n, 1, 2, 3, out);
    std::cout << out.str();
    return 0;
}