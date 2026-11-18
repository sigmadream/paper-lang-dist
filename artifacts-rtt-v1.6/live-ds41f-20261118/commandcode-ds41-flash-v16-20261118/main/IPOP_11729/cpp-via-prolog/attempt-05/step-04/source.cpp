#include <bits/stdc++.h>
using namespace std;

string out;

void hanoi(int n, int a, int b, int c) {
    if (n == 1) {
        out += to_string(a);
        out += ' ';
        out += to_string(c);
        out += '\n';
        return;
    }
    hanoi(n - 1, a, c, b);
    out += to_string(a);
    out += ' ';
    out += to_string(c);
    out += '\n';
    hanoi(n - 1, b, a, c);
}

int main() {
    int n;
    if (!(cin >> n)) return 0;
    out.reserve(7000000);
    out += to_string((1 << n) - 1);
    out += '\n';
    hanoi(n, 1, 2, 3);
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}