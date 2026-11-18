#include <bits/stdc++.h>
using namespace std;

static void hanoi(int k, int start, int mid, int end, string& out) {
    if (k == 1) {
        out += to_string(start);
        out.push_back(' ');
        out += to_string(end);
        out.push_back('\n');
        return;
    }

    hanoi(k - 1, start, end, mid, out);

    out += to_string(start);
    out.push_back(' ');
    out += to_string(end);
    out.push_back('\n');

    hanoi(k - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    string out;
    out.reserve((1u << n) * 4u + 16u);

    out += to_string((1 << n) - 1);
    out.push_back('\n');

    hanoi(n, 1, 2, 3, out);

    cout.write(out.data(), static_cast<streamsize>(out.size()));
    return 0;
}