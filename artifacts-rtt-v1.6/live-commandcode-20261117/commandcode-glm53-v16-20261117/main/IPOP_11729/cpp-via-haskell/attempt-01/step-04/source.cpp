#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e, vector<pair<int,int>>& out) {
    if (n == 1) { out.push_back({s, e}); return; }
    hanoi(n - 1, s, e, m, out);
    out.push_back({s, e});
    hanoi(n - 1, m, s, e, out);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    int n = 0;
    bool found = false;
    istringstream iss(line);
    string w;
    while (iss >> w) {
        try {
            size_t pos;
            int v = stoi(w, &pos);
            if (pos == w.size()) { n = v; found = true; break; }
        } catch (...) {}
    }
    if (!found || n < 1) return 0;
    vector<pair<int,int>> moves;
    moves.reserve((1u << n) - 1);
    hanoi(n, 1, 2, 3, moves);
    cout << moves.size() << "\n";
    for (auto& p : moves) cout << p.first << " " << p.second << "\n";
    return 0;
}