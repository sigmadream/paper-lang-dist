#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;

    vector<string> out;
    out.reserve(t);

    for (int i = 0; i < t; ++i) {
        string s;
        cin >> s;

        int bal = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++bal;
            } else {
                --bal;
            }
            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) valid = false;
        out.push_back(valid ? "YES" : "NO");
    }

    for (int i = 0; i < (int)out.size(); ++i) {
        if (i > 0) cout << '\n';
        cout << out[i];
    }

    return 0;
}