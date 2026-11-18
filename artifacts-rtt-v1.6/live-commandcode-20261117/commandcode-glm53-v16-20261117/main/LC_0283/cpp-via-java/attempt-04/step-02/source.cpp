#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int write = 0;
    for (int read = 0; read < n; read++) {
        if (a[read] != 0) {
            swap(a[write], a[read]);
            write++;
        }
    }
    string out;
    for (int i = 0; i < n; i++) {
        if (i > 0) out += ' ';
        out += to_string(a[i]);
    }
    out += '\n';
    cout << out;
    return 0;
}