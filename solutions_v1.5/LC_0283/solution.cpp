#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    vector<long long> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    int write_idx = 0;
    for (int read_idx = 0; read_idx < n; ++read_idx) {
        if (a[read_idx] != 0) {
            swap(a[write_idx++], a[read_idx]);
        }
    }

    for (int i = 0; i < n; ++i) {
        cout << (i > 0 ? " " : "") << a[i];
    }
    cout << "\n";

    return 0;
}
