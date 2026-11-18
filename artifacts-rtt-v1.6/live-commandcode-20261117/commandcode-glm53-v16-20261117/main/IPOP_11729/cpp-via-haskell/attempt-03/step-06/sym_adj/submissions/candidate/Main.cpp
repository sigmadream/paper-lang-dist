#include <iostream>
#include <string>
#include <vector>

void hanoi(int n, int s, int m, int e, std::vector<std::pair<int,int>>& moves) {
    if (n == 1) { moves.push_back({s, e}); return; }
    hanoi(n - 1, s, e, m, moves);
    moves.push_back({s, e});
    hanoi(n - 1, m, s, e, moves);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n;
    std::cin >> n;
    std::vector<std::pair<int,int>> moves;
    moves.reserve((1u << n) - 1);
    hanoi(n, 1, 2, 3, moves);
    std::string out;
    out += std::to_string(moves.size());
    out += '\n';
    for (auto& p : moves) {
        out += std::to_string(p.first);
        out += ' ';
        out += std::to_string(p.second);
        out += '\n';
    }
    std::cout << out;
    return 0;
}