#include <bits/stdc++.h>
using namespace std;

static bool readLine(string& out) {
    if (!getline(cin, out)) return false;
    if (!out.empty() && out.back() == '\r') out.pop_back();
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    if (!readLine(s) || !readLine(t)) {
        cout << 0 << '\n';
        return 0;
    }

    if (s.size() != t.size()) {
        cout << 0 << '\n';
        return 0;
    }

    int counts[26] = {0};
    for (size_t i = 0; i < s.size(); ++i) {
        ++counts[s[i] - 'a'];
        --counts[t[i] - 'a'];
    }

    for (int count : counts) {
        if (count != 0) {
            cout << 0 << '\n';
            return 0;
        }
    }

    cout << 1 << '\n';
    return 0;
}