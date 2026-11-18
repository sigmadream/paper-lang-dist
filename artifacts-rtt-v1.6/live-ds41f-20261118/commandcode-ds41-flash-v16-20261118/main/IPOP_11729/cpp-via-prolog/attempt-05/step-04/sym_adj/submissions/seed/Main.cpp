#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int a, int b, int c, string& out) {
    if (n == 1) {
        out += to_string(a);
        out += ' ';
        out += to_string(c);
        out += '\n';
        return;
    }

    hanoi(n - 1, a, c, b, out);

    out += to_string(a);
    out += ' ';
    out += to_string(c);
    out += '\n';

    hanoi(n - 1, b, a, c, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    long long count = (1LL << N) - 1;

    string out;
    out.reserve(static_cast<size_t>(count) * 6 + 32);

    out += to_string(count);
    out += '\n';

    hanoi(N, 1, 2, 3, out);

    cout << out;
    return 0;
}