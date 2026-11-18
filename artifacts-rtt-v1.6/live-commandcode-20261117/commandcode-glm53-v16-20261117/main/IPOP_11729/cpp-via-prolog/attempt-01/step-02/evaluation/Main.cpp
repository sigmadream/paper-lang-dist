#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int start, int mid, int end_, vector<pair<int,int>>& moves) {
    if (n == 1) { moves.push_back({start, end_}); return; }
    hanoi(n-1, start, end_, mid, moves);
    moves.push_back({start, end_});
    hanoi(n-1, mid, start, end_, moves);
}

int main() {
    int n;
    if (!(cin >> n)) return 0;
    if (n < 1) return 0;
    vector<pair<int,int>> moves;
    hanoi(n, 1, 2, 3, moves);
    cout << moves.size() << "\n";
    for (auto& [a, b] : moves) cout << a << " " << b << "\n";
    return 0;
}