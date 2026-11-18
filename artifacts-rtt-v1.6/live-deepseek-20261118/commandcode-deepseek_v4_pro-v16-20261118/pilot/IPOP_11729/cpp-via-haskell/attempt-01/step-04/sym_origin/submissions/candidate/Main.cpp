#include <iostream>
#include <vector>
#include <utility>

void hanoi(int n, int start, int mid, int end, std::vector<std::pair<int, int>>& moves) {
    if (n == 1) {
        moves.push_back({start, end});
        return;
    }
    hanoi(n - 1, start, end, mid, moves);
    moves.push_back({start, end});
    hanoi(n - 1, mid, start, end, moves);
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::pair<int, int>> moves;
    hanoi(n, 1, 2, 3, moves);

    std::cout << moves.size() << '\n';
    for (const auto& move : moves) {
        std::cout << move.first << ' ' << move.second << '\n';
    }
    return 0;
}