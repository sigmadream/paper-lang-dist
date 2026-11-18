#include <bits/stdc++.h>
using namespace std;

string out;

void appendInt(long long x) {
    char buf[24];
    int len = 0;

    if (x == 0) {
        buf[len++] = '0';
    } else {
        while (x > 0) {
            buf[len++] = char('0' + (x % 10));
            x /= 10;
        }
        reverse(buf, buf + len);
    }

    out.append(buf, len);
}

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        appendInt(start);
        out.push_back(' ');
        appendInt(end);
        out.push_back('\n');
        return;
    }

    hanoi(n - 1, start, end, mid);

    appendInt(start);
    out.push_back(' ');
    appendInt(end);
    out.push_back('\n');

    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    out.reserve(static_cast<size_t>(count) * 6 + 32);

    appendInt(count);
    out.push_back('\n');

    hanoi(n, 1, 2, 3);

    cout << out;
    return 0;
}