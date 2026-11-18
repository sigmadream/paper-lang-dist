#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }

    vector<int> result;
    result.reserve(n);

    int zeroCount = 0;
    for (int x : arr) {
        if (x != 0) {
            result.push_back(x);
        } else {
            ++zeroCount;
        }
    }

    for (int i = 0; i < zeroCount; ++i) {
        result.push_back(0);
    }

    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) cout << ' ';
        cout << result[i];
    }
    cout << '\n';

    return 0;
}