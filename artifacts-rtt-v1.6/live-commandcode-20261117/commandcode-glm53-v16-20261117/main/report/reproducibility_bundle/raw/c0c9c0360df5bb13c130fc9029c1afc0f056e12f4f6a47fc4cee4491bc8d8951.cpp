#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    int write = 0;
    for (int read = 0; read < n; read++) {
        if (a[read] != 0) {
            swap(a[write], a[read]);
            write++;
        }
    }
    for (int i = 0; i < n; i++) {
        if (i > 0) putchar(' ');
        printf("%lld", a[i]);
    }
    putchar('\n');
    return 0;
}