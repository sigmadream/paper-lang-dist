#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int start, int mid, int end, vector<pair<int,int>>& moves) {
    if (n == 1) { moves.push_back({start, end}); return; }
    hanoi(n - 1, start, end, mid, moves);
    moves.push_back({start, end});
    hanoi(n - 1, mid, start, end, moves);
}

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<pair<int,int>> moves;
    hanoi(n, 1, 2, 3, moves);
    ostringstream oss;
    oss << moves.size() << '\n';
    for (auto& [a, b] : moves) oss << a << ' ' << b << '\n';
    cout << oss.str();
    return 0;
}