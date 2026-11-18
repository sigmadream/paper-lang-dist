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
    getline(cin, line);
    size_t i = 0;
    while (i < line.size() && !isdigit((unsigned char)line[i])) i++;
    size_t start = i;
    while (i < line.size() && isdigit((unsigned char)line[i])) i++;
    long long n = stoll(line.substr(start, i - start));
    vector<pair<int,int>> moves;
    if (n > 0) hanoi((int)n, 1, 2, 3, moves);
    long long count = (1LL << n) - 1;
    cout << count << "\n";
    for (auto& p : moves) cout << p.first << " " << p.second << "\n";
    return 0;
}