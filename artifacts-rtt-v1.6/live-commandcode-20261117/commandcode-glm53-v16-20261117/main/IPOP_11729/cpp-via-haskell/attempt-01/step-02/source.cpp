#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e, vector<pair<int,int>>& out) {
    if (n == 1) { out.push_back({s, e}); return; }
    hanoi(n - 1, s, e, m, out);
    out.push_back({s, e});
    hanoi(n - 1, m, s, e, out);
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    istringstream iss(line);
    int n;
    if (!(iss >> n) || n < 1) return 0;
    vector<pair<int,int>> moves;
    hanoi(n, 1, 2, 3, moves);
    ostringstream oss;
    oss << moves.size() << '\n';
    for (auto& [a, b] : moves) oss << a << ' ' << b << '\n';
    cout << oss.str();
    return 0;
}