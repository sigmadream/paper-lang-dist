#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    if (!(cin >> n)) return 0;
    vector<int> arr(n + 1);
    arr[0] = 0;
    for (long long i = 1; i <= n; ++i) {
        arr[i] = arr[i / 2] + (int)(i % 2);
    }
    for (size_t i = 0; i < arr.size(); ++i) {
        if (i) cout << ' ';
        cout << arr[i];
    }
    cout << '\n';
    return 0;
}