#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int a, int b, int c, string &out) {
    if (n == 1) { out += to_string(a) + " " + to_string(c) + "\n"; return; }
    hanoi(n - 1, a, c, b, out);
    out += to_string(a) + " " + to_string(c) + "\n";
    hanoi(n - 1, b, a, c, out);
}

int main() {
    int n;
    if (!(cin >> n)) return 0;
    if (n < 1) return 0;
    string out;
    hanoi(n, 1, 2, 3, out);
    cout << ((1LL << n) - 1) << "\n" << out;
    return 0;
}