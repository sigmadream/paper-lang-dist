#include <iostream>
#include <vector>
#include <utility>

void hanoi(int n, int start, int mid, int end, std::vector<std::pair<int,int>>& moves) {
    if (n == 1) {
        moves.emplace_back(start, end);
        return;
    }
    hanoi(n - 1, start, end, mid, moves);
    moves.emplace_back(start, end);
    hanoi(n - 1, mid, start, end, moves);
}

int main() {
    int n;
    std::cin >> n;

    std::vector<std::pair<int,int>> moves;
    moves.reserve((1 << n) - 1);
    hanoi(n, 1, 2, 3, moves);

    std::cout << moves.size() << '\n';
    for (const auto& [from, to] : moves) {
        std::cout << from << ' ' << to << '\n';
    }

    return 0;
}