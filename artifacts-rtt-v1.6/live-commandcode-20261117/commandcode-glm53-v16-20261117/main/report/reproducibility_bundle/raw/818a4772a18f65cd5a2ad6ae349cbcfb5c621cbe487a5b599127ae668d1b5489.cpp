#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> arr(n);
    for (int i = 0; i < n; i++) cin >> arr[i];
    int write = 0;
    for (int read = 0; read < n; read++) {
        if (arr[read] != 0) {
            swap(arr[write], arr[read]);
            write++;
        }
    }
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << ' ';
        cout << arr[i];
    }
    cout << '\n';
    return 0;
}