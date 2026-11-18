#include <iostream>
#include <string>

static void hanoi(int n, int start, int mid, int end, std::string& out) {
    if (n == 1) {
        out += std::to_string(start);
        out += ' ';
        out += std::to_string(end);
        out += '\n';
        return;
    }

    hanoi(n - 1, start, end, mid, out);
    out += std::to_string(start);
    out += ' ';
    out += std::to_string(end);
    out += '\n';
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    int moves = (1 << n) - 1;

    std::string out;
    out.reserve(4 * static_cast<size_t>(moves) + 16);
    out += std::to_string(moves);
    out += '\n';

    hanoi(n, 1, 2, 3, out);

    std::cout << out;
    return 0;
}