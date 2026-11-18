#include <cstdio>

static void hanoi(int n, int from, int via, int to) {
    if (n == 1) {
        std::printf("%d %d\n", from, to);
        return;
    }
    hanoi(n - 1, from, to, via);
    std::printf("%d %d\n", from, to);
    hanoi(n - 1, via, from, to);
}

int main() {
    int N;
    if (std::scanf("%d", &N) != 1) return 0;
    int count = (1 << N) - 1;
    std::printf("%d\n", count);
    hanoi(N, 1, 2, 3);
    return 0;
}