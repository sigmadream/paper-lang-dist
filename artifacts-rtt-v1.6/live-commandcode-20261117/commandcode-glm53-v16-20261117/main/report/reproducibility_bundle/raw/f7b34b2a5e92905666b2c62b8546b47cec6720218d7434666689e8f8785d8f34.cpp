#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    istringstream iss(line);
    long long n;
    if (!(iss >> n) || n < 0) return 0;
    vector<int> res;
    res.reserve(n + 1);
    for (long long i = 0; i <= n; ++i) {
        if (i == 0) res.push_back(0);
        else res.push_back(res[i / 2] + (int)(i % 2));
    }
    for (size_t i = 0; i < res.size(); ++i) {
        if (i) cout << ' ';
        cout << res[i];
    }
    cout << '\n';
    return 0;
}