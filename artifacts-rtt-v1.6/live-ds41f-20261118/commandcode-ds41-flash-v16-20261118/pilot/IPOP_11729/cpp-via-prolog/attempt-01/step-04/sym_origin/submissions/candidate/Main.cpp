#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e) {
    if (n == 1) {
        cout << s << ' ' << e << '\n';
        return;
    }
    hanoi(n - 1, s, e, m);
    cout << s << ' ' << e << '\n';
    hanoi(n - 1, m, s, e);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    int moves = (1 << N) - 1;
    cout << moves << '\n';
    hanoi(N, 1, 2, 3);

    return 0;
}