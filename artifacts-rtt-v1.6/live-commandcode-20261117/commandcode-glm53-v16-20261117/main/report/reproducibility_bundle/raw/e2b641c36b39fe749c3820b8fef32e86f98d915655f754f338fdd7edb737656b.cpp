#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int,int>> moves;
    moves.reserve(1 << n);
    function<void(int,int,int,int)> hanoi = [&](int k, int s, int m, int e) {
        if (k == 1) { moves.push_back({s, e}); return; }
        hanoi(k - 1, s, e, m);
        moves.push_back({s, e});
        hanoi(k - 1, m, s, e);
    };
    hanoi(n, 1, 2, 3);
    cout << moves.size() << "\n";
    for (auto& [a, b] : moves) cout << a << " " << b << "\n";
    return 0;
}