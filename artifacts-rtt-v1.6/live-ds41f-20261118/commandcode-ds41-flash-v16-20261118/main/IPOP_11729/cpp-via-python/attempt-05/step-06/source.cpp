#include <bits/stdc++.h>
using namespace std;

static void hanoi(int k, int start, int mid, int end, string &out) {
    if (k == 0) return;
    if (k == 1) {
        out += to_string(start);
        out += ' ';
        out += to_string(end);
        out += '\n';
        return;
    }

    hanoi(k - 1, start, end, mid, out);

    out += to_string(start);
    out += ' ';
    out += to_string(end);
    out += '\n';

    hanoi(k - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long moves = (1LL << n) - 1;

    string out;
    out.reserve(static_cast<size_t>(moves) * 4 + 32);

    out += to_string(moves);
    out += '\n';

    hanoi(n, 1, 2, 3, out);

    cout << out;
    return 0;
}