#include <bits/stdc++.h>
using namespace std;

static void strip_cr(string& s) {
    if (!s.empty() && s.back() == '\r') s.pop_back();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    if (!getline(cin, s)) s.clear();
    else strip_cr(s);

    if (!getline(cin, t)) t.clear();
    else strip_cr(t);

    sort(s.begin(), s.end());
    sort(t.begin(), t.end());

    cout << (s == t ? 1 : 0) << '\n';
    return 0;
}