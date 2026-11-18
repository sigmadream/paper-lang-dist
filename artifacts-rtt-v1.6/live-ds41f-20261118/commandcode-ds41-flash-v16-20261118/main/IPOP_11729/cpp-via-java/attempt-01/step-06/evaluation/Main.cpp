#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int start, int mid, int end, string& sb) {
    if (n == 1) {
        sb += to_string(start);
        sb += ' ';
        sb += to_string(end);
        sb += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid, sb);
    sb += to_string(start);
    sb += ' ';
    sb += to_string(end);
    sb += '\n';
    hanoi(n - 1, mid, start, end, sb);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    string sb;
    sb += to_string((1LL << n) - 1);
    sb += '\n';
    hanoi(n, 1, 2, 3, sb);

    cout << sb;
    return 0;
}