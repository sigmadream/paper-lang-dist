#include <cstdio>
#include <string>

static std::string moves;

static void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        moves += std::to_string(start);
        moves += ' ';
        moves += std::to_string(end);
        moves += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid);
    moves += std::to_string(start);
    moves += ' ';
    moves += std::to_string(end);
    moves += '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    printf("%lld\n", count);
    fputs(moves.c_str(), stdout);
    return 0;
}