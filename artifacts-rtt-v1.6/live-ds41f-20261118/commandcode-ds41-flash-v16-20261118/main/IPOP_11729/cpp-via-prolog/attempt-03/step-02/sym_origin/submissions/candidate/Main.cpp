#include <cstdio>

static void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        std::printf("%d %d\n", start, end);
        return;
    }
    hanoi(n - 1, start, end, mid);
    std::printf("%d %d\n", start, end);
    hanoi(n - 1, mid, start, end);
}

int main() {
    int N;
    if (std::scanf("%d", &N) != 1) return 0;

    long long count = (1LL << N) - 1;
    std::printf("%lld\n", count);

    hanoi(N, 1, 2, 3);
    return 0;
}