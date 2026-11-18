#include <iostream>
#include <string>

std::string moves;

void add_move(int from, int to) {
    moves.push_back(static_cast<char>('0' + from));
    moves.push_back(' ');
    moves.push_back(static_cast<char>('0' + to));
    moves.push_back('\n');
}

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        add_move(start, end);
        return;
    }
    hanoi(n - 1, start, end, mid);
    add_move(start, end);
    hanoi(n - 1, mid, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    unsigned long long total = (1ULL << n) - 1;
    moves.reserve(static_cast<std::size_t>(total) * 4);

    hanoi(n, 1, 2, 3);

    std::cout << total << '\n';
    std::cout << moves;

    return 0;
}