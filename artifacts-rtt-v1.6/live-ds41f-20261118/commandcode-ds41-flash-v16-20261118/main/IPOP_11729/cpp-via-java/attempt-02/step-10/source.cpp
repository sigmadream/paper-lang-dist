#include <bits/stdc++.h>
using namespace std;

static void hanoi(int n, int start, int mid, int end, string& out) {
    if (n == 1) {
        out += to_string(start);
        out.push_back(' ');
        out += to_string(end);
        out.push_back('\n');
        return;
    }

    hanoi(n - 1, start, end, mid, out);
    out += to_string(start);
    out.push_back(' ');
    out += to_string(end);
    out.push_back('\n');
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    string out;
    out.reserve(static_cast<size_t>(count * 4 + 32));

    out += to_string(count);
    out.push_back('\n');

    hanoi(n, 1, 2, 3, out);

    cout << out;
    return 0;
}