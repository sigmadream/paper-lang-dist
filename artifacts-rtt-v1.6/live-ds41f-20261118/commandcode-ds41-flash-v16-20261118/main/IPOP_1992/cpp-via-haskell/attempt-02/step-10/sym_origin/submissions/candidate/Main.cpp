#include <bits/stdc++.h>
using namespace std;

string solve(const vector<string>& arr, int r, int c, int size) {
    char first = arr[r][c];
    bool same = true;

    for (int i = 0; i < size && same; ++i) {
        for (int j = 0; j < size; ++j) {
            if (arr[r + i][c + j] != first) {
                same = false;
                break;
            }
        }
    }

    if (same) return string(1, first);

    int half = size / 2;
    return "(" +
           solve(arr, r, c, half) +
           solve(arr, r, c + half, half) +
           solve(arr, r + half, c, half) +
           solve(arr, r + half, c + half, half) +
           ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<string> arr(N);
    for (int i = 0; i < N; ++i) {
        cin >> arr[i];
    }

    cout << solve(arr, 0, 0, N) << '\n';
    return 0;
}