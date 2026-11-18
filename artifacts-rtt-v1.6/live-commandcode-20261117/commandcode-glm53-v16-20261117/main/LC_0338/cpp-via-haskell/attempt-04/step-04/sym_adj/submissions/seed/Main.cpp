#include <bits/stdc++.h>
using namespace std;

int main() {
    int n = 0;
    if (!(cin >> n)) n = 0;
    vector<int> arr(n + 1);
    arr[0] = 0;
    for (int i = 1; i <= n; ++i) arr[i] = arr[i / 2] + (i % 2);
    for (int i = 0; i <= n; ++i) {
        if (i) cout << ' ';
        cout << arr[i];
    }
    cout << '\n';
    return 0;
}