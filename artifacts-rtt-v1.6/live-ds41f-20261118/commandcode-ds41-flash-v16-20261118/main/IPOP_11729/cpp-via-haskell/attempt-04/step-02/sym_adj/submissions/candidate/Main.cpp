#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int a, int b, int c, vector<pair<int,int>>& moves) {
    if (n == 0) return;
    if (n == 1) {
        moves.emplace_back(a, c);
        return;
    }
    hanoi(n - 1, a, c, b, moves);
    moves.emplace_back(a, c);
    hanoi(n - 1, b, a, c, moves);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    long long count = (1LL << n) - 1;
    vector<pair<int,int>> moves;
    moves.reserve(static_cast<size_t>(count));
    hanoi(n, 1, 2, 3, moves);
    string out;
    out.reserve(20 + static_cast<size_t>(count) * 6);
    out += to_string(count);
    out += '\n';
    for (const auto& p : moves) {
        out += to_string(p.first);
        out += ' ';
        out += to_string(p.second);
        out += '\n';
    }
    cout << out;
    return 0;
}