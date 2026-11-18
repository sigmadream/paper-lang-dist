#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int start, int mid, int end, ostream& out) {
    if (n == 1) {
        out << start << ' ' << end << '\n';
        return;
    }
    hanoi(n - 1, start, end, mid, out);
    out << start << ' ' << end << '\n';
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    cout << ((1LL << n) - 1) << '\n';
    hanoi(n, 1, 2, 3, cout);
    return 0;
}