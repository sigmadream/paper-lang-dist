#include <bits/stdc++.h>
using namespace std;

static void hanoi(int n, int start, int mid, int end, string& out) {
    if (n == 1) {
        out += to_string(start);
        out += ' ';
        out += to_string(end);
        out += '\n';
        return;
    }

    hanoi(n - 1, start, end, mid, out);
    out += to_string(start);
    out += ' ';
    out += to_string(end);
    out += '\n';
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    int moves = (1 << n) - 1;

    string out;
    out.reserve(max(16, moves * 4 + 16));
    out += to_string(moves);
    out += '\n';

    hanoi(n, 1, 2, 3, out);

    cout << out;
    return 0;
}