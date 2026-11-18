#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int from, int mid, int to) {
    if (n == 1) {
        cout << from << ' ' << to << '\n';
        return;
    }
    hanoi(n - 1, from, to, mid);
    cout << from << ' ' << to << '\n';
    hanoi(n - 1, mid, from, to);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    cout << ((1LL << n) - 1) << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}