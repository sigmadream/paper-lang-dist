#include <iostream>
#include <string>
#include <cstdint>

static void hanoi(int n, int start, int mid, int end, std::string& moves) {
    if (n == 1) {
        moves += std::to_string(start);
        moves += ' ';
        moves += std::to_string(end);
        moves += '\n';
        return;
    }

    hanoi(n - 1, start, end, mid, moves);

    moves += std::to_string(start);
    moves += ' ';
    moves += std::to_string(end);
    moves += '\n';

    hanoi(n - 1, mid, start, end, moves);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::string moves;
    moves.reserve((1u << n) * 5);

    hanoi(n, 1, 2, 3, moves);

    const std::uint64_t count = (1ULL << n) - 1;

    std::string output;
    output.reserve(32 + moves.size());
    output += std::to_string(count);
    output += '\n';
    output += moves;

    std::cout << output;
    return 0;
}