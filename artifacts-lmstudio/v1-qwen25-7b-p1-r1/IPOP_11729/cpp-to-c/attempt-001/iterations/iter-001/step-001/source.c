#include <stdio.h>

void hanoi(int n, int start, int mid, int end, int moves[][2], int *move_count) {
    if (n == 1) {
        moves[*move_count][0] = start;
        moves[*move_count][1] = end;
        (*move_count)++;
        return;
    }
    hanoi(n - 1, start, end, mid, moves, move_count);
    moves[*move_count][0] = start;
    moves[*move_count][1] = end;
    (*move_count)++;
    hanoi(n - 1, mid, start, end, moves, move_count);
}

int main() {
    int n;
    scanf("%d", &n);
    int moves[1048576][2]; // 2^20
    int move_count = 0;
    hanoi(n, 1, 2, 3, moves, &move_count);
    printf("%d\n", move_count);
    for (int i = 0; i < move_count; i++) {
        printf("%d %d\n", moves[i][0], moves[i][1]);
    }
    return 0;
}
