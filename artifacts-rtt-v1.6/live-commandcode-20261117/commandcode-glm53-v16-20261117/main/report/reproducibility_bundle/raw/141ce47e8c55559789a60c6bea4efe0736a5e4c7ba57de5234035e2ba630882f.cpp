#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int a, int b, int c, vector<pair<int,int>>& out) {
    if (n == 1) { out.push_back({a, c}); return; }
    hanoi(n - 1, a, c, b, out);
    out.push_back({a, c});
    hanoi(n - 1, b, a, c, out);
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    long long n = stoll(line);
    if (n < 1) return 0;
    long long m = (1LL << n) - 1;
    cout << m << "\n";
    vector<pair<int,int>> moves;
    moves.reserve(m);
    hanoi((int)n, 1, 2, 3, moves);
    for (auto& p : moves) cout << p.first << " " << p.second << "\n";
    return 0;
}