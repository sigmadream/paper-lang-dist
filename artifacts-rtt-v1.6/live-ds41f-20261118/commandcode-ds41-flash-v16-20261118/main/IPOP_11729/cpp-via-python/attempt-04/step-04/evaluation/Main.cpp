#include <iostream>
#include <string>

void hanoi(int n, int start, int mid, int end, std::string& moves) {
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

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    int n = std::stoi(line);

    std::string moves;
    moves.reserve(static_cast<size_t>(1u << n) * 6);
    hanoi(n, 1, 2, 3, moves);

    long long count = (1LL << n) - 1;
    std::cout << count << '\n';
    std::cout << moves;

    return 0;
}