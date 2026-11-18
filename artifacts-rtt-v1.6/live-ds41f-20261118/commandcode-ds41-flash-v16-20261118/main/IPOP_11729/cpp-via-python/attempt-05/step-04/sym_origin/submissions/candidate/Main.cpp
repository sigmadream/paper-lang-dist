#include <iostream>

using namespace std;

void hanoi(int k, int start, int mid, int end) {
    if (k == 0) return;
    if (k == 1) {
        cout << start << ' ' << end << '\n';
        return;
    }

    hanoi(k - 1, start, end, mid);
    cout << start << ' ' << end << '\n';
    hanoi(k - 1, mid, start, end);
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