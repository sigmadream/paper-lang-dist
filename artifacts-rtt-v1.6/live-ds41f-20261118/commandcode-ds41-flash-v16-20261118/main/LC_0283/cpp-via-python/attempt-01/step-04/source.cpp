#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> data;
    string tok;
    while (cin >> tok) data.push_back(tok);
    if (data.empty()) return 0;

    int n = stoi(data[0]);
    vector<int> a;
    for (int i = 1; i < (int)data.size() && i <= n; ++i) {
        a.push_back(stoi(data[i]));
    }

    int write = 0;
    int sz = (int)a.size();
    for (int read = 0; read < n && read < sz; ++read) {
        if (a[read] != 0) {
            swap(a[write], a[read]);
            ++write;
        }
    }

    for (size_t i = 0; i < a.size(); ++i) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';

    return 0;
}