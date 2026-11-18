#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e, ostream& out) {
    if (n == 1) {
        out << s << ' ' << e << '\n';
        return;
    }
    hanoi(n - 1, s, e, m, out);
    out << s << ' ' << e << '\n';
    hanoi(n - 1, m, s, e, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    long long count = (1LL << N) - 1;
    cout << count << '\n';
    hanoi(N, 1, 2, 3, cout);

    return 0;
}