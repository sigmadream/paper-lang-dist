#include <iostream>
#include <string>

std::string output;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        output += std::to_string(start);
        output += ' ';
        output += std::to_string(end);
        output += '\n';
        return;
    }

    hanoi(n - 1, start, end, mid);

    output += std::to_string(start);
    output += ' ';
    output += std::to_string(end);
    output += '\n';

    hanoi(n - 1, mid, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    int count = (1 << n) - 1;

    output.reserve(static_cast<size_t>(count) * 5 + 16);
    output += std::to_string(count);
    output += '\n';

    hanoi(n, 1, 2, 3);

    std::cout << output;
    return 0;
}