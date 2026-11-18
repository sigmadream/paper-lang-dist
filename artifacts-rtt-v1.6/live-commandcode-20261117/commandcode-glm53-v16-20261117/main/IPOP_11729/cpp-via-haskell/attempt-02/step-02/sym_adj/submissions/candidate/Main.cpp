#include <cstdio>
#include <vector>
#include <utility>

std::vector<std::pair<int,int>> moves;

void hanoi(int n, int s, int m, int e) {
    if (n == 1) { moves.push_back({s, e}); return; }
    hanoi(n - 1, s, e, m);
    moves.push_back({s, e});
    hanoi(n - 1, m, s, e);
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    hanoi(n, 1, 2, 3);
    printf("%zu\n", moves.size());
    for (auto& p : moves) printf("%d %d\n", p.first, p.second);
    return 0;
}