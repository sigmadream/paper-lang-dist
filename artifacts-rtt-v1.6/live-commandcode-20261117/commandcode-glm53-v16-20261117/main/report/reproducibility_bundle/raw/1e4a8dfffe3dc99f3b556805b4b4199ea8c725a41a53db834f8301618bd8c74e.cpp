#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e, ostream& out) {
    if (n == 1) { out << s << ' ' << e << '\n'; return; }
    hanoi(n - 1, s, e, m, out);
    out << s << ' ' << e << '\n';
    hanoi(n - 1, m, s, e, out);
}

int main() {
    int n;
    cin >> n;
    long long cnt = (1LL << n) - 1;
    ostringstream buf;
    buf << cnt << '\n';
    hanoi(n, 1, 2, 3, buf);
    cout << buf.str();
    return 0;
}