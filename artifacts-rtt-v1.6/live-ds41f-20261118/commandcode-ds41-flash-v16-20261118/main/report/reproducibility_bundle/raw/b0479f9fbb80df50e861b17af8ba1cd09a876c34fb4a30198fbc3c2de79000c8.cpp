#include <iostream>
#include <string>

void hanoi(int n, int start, int middle, int end, std::string& out) {
    if (n == 1) {
        out += std::to_string(start);
        out += ' ';
        out += std::to_string(end);
        out += '\n';
        return;
    }

    hanoi(n - 1, start, end, middle, out);

    out += std::to_string(start);
    out += ' ';
    out += std::to_string(end);
    out += '\n';

    hanoi(n - 1, middle, start, end, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::string out;
    out.reserve(8 * 1024 * 1024);

    out += std::to_string((1 << n) - 1);
    out += '\n';

    hanoi(n, 1, 2, 3, out);

    std::cout << out;
    return 0;
}