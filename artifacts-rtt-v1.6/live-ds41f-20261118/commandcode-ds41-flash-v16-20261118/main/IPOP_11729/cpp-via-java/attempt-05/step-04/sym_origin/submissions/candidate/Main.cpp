#include <bits/stdc++.h>
using namespace std;

static string out;

static void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        out.push_back(char('0' + start));
        out.push_back(' ');
        out.push_back(char('0' + end));
        out.push_back('\n');
        return;
    }

    hanoi(n - 1, start, end, mid);

    out.push_back(char('0' + start));
    out.push_back(' ');
    out.push_back(char('0' + end));
    out.push_back('\n');

    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    out.reserve((size_t)(count * 6 + 32));

    out += to_string(count);
    out.push_back('\n');

    hanoi(n, 1, 2, 3);

    cout << out;
    return 0;
}