#include <bits/stdc++.h>
using namespace std;

static string out;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        out += char('0' + start);
        out += ' ';
        out += char('0' + end);
        out += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid);
    out += char('0' + start);
    out += ' ';
    out += char('0' + end);
    out += '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    unsigned long long cnt = (n >= 64) ? 0ULL : ((1ULL << n) - 1);
    hanoi(n, 1, 2, 3);
    cout << cnt << '\n' << out;
    return 0;
}