#include <iostream>
#include <vector>
#include <utility>

void hanoi(int n, int from, int aux, int to, std::vector<std::pair<int, int>>& moves) {
    if (n == 1) {
        moves.push_back({from, to});
        return;
    }
    hanoi(n - 1, from, to, aux, moves);
    moves.push_back({from, to});
    hanoi(n - 1, aux, from, to, moves);
}

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<std::pair<int, int>> moves;
    moves.reserve((size_t{1} << n) - 1);

    hanoi(n, 1, 2, 3, moves);

    std::cout << moves.size() << '\n';
    for (const auto& [from, to] : moves) {
        std::cout << from << ' ' << to << '\n';
    }

    return 0;
}