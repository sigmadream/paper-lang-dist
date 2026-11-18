#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int,int>> moves;
    function<void(int,int,int,int)> hanoi = [&](int n, int s, int m, int e) {
        if (n == 1) { moves.push_back({s, e}); return; }
        hanoi(n-1, s, e, m);
        moves.push_back({s, e});
        hanoi(n-1, m, s, e);
    };
    hanoi(n, 1, 2, 3);
    cout << moves.size() << "\n";
    for (auto& [a, b] : moves) cout << a << " " << b << "\n";
    return 0;
}