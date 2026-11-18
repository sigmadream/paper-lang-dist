#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<pair<int, int>> moves;
    moves.reserve((1LL << n) - 1);

    function<void(int, int, int, int)> hanoi = [&](int k, int start, int mid, int end) {
        if (k == 1) {
            moves.push_back({start, end});
            return;
        }
        hanoi(k - 1, start, end, mid);
        moves.push_back({start, end});
        hanoi(k - 1, mid, start, end);
    };

    long long count = (1LL << n) - 1;
    hanoi(n, 1, 2, 3);

    cout << count << "\n";
    for (const auto &move : moves) {
        cout << move.first << " " << move.second << "\n";
    }

    return 0;
}