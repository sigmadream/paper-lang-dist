#include <bits/stdc++.h>
using namespace std;

string solve(const vector<string>& arr, int r, int c, int size) {
    char first = arr[r][c];
    bool same = true;

    for (int i = r; i < r + size && same; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (arr[i][j] != first) {
                same = false;
                break;
            }
        }
    }

    if (same) {
        return string(1, first);
    }

    int half = size / 2;
    return "("
         + solve(arr, r, c, half)
         + solve(arr, r, c + half, half)
         + solve(arr, r + half, c, half)
         + solve(arr, r + half, c + half, half)
         + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<string> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }

    cout << solve(arr, 0, 0, n) << '\n';
    return 0;
}