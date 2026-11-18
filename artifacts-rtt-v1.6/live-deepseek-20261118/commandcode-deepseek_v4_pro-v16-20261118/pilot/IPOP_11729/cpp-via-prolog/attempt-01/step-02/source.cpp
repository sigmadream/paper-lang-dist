#include <iostream>
#include <vector>
#include <utility>

void hanoi(int n, int from, int mid, int to, std::vector<std::pair<int,int>>& moves) {
    if (n == 1) {
        moves.emplace_back(from, to);
        return;
    }
    hanoi(n - 1, from, to, mid, moves);
    moves.emplace_back(from, to);
    hanoi(n - 1, mid, from, to, moves);
}

int main() {
    int N;
    if (!(std::cin >> N)) {
        return 0;
    }
    std::vector<std::pair<int,int>> moves;
    hanoi(N, 1, 2, 3, moves);
    std::cout << moves.size() << '\n';
    for (const auto& m : moves) {
        std::cout << m.first << ' ' << m.second << '\n';
    }
    return 0;
}