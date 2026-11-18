#include <bits/stdc++.h>
using namespace std;

string solve(const vector<string>& rows) {
    int n = (int)rows.size();
    char first = rows[0][0];
    bool same = true;

    for (int i = 0; i < n && same; ++i) {
        for (int j = 0; j < n; ++j) {
            if (rows[i][j] != first) {
                same = false;
                break;
            }
        }
    }

    if (same) return string(1, first);

    int h = n / 2;
    vector<string> tl(h), tr(h), bl(h), br(h);

    for (int i = 0; i < h; ++i) {
        tl[i] = rows[i].substr(0, h);
        tr[i] = rows[i].substr(h, h);
    }
    for (int i = 0; i < h; ++i) {
        bl[i] = rows[h + i].substr(0, h);
        br[i] = rows[h + i].substr(h, h);
    }

    return "(" + solve(tl) + solve(tr) + solve(bl) + solve(br) + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<string> rows(n);
    for (int i = 0; i < n; ++i) {
        cin >> rows[i];
    }

    cout << solve(rows) << '\n';
    return 0;
}