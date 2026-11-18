#include <bits/stdc++.h>
using namespace std;

void hanoi(int count, int start, int mid, int end, string& out) {
    if (count == 1) {
        out += to_string(start);
        out += ' ';
        out += to_string(end);
        out += '\n';
        return;
    }

    hanoi(count - 1, start, end, mid, out);

    out += to_string(start);
    out += ' ';
    out += to_string(end);
    out += '\n';

    hanoi(count - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    string out;
    out.reserve(static_cast<size_t>((1 << n) - 1) * 4 + 16);

    out += to_string((1 << n) - 1);
    out += '\n';

    hanoi(n, 1, 2, 3, out);

    cout << out;
    return 0;
}