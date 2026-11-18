#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e, vector<pair<int,int>>& out) {
    if (n == 1) { out.push_back({s, e}); return; }
    hanoi(n - 1, s, e, m, out);
    out.push_back({s, e});
    hanoi(n - 1, m, s, e, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    while (cin >> n) {
        if (n >= 1) {
            vector<pair<int,int>> moves;
            moves.reserve((size_t)1 << n);
            hanoi(n, 1, 2, 3, moves);
            cout << moves.size() << "\n";
            for (auto& p : moves) cout << p.first << " " << p.second << "\n";
            break;
        }
    }
    return 0;
}