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
    string out = to_string(moves.size());
    for (auto& [a, b] : moves) {
        out += '\n';
        out += to_string(a);
        out += ' ';
        out += to_string(b);
    }
    out += '\n';
    cout << out;
    return 0;
}