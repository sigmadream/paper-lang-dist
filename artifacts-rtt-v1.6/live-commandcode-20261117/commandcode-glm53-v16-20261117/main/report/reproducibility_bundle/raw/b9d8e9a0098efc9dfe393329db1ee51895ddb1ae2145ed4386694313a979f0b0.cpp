#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int a, int b, int c, string &out) {
    if (n == 1) {
        out += to_string(a);
        out += ' ';
        out += to_string(c);
        out += '\n';
        return;
    }
    hanoi(n - 1, a, c, b, out);
    out += to_string(a);
    out += ' ';
    out += to_string(c);
    out += '\n';
    hanoi(n - 1, b, a, c, out);
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    if (n < 1) return 0;
    printf("%llu\n", (unsigned long long)((1ULL << n) - 1));
    string out;
    out.reserve((size_t)(1u << n) * 4);
    hanoi(n, 1, 2, 3, out);
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}