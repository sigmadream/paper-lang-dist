#include <bits/stdc++.h>
using namespace std;

static bool is_ws(unsigned char c) {
    return c == 9 || c == 10 || c == 11 || c == 12 || c == 13 || c == 32;
}

static string trim_codes(const string& s) {
    size_t l = 0, r = s.size();
    while (l < r && is_ws(static_cast<unsigned char>(s[l]))) ++l;
    while (r > l && is_ws(static_cast<unsigned char>(s[r - 1]))) --r;
    return s.substr(l, r - l);
}

static bool valid_parens(const string& s) {
    if (s.empty()) return false;

    int balance = 0;
    for (char ch : s) {
        if (ch == '(') {
            ++balance;
        } else if (ch == ')') {
            if (balance == 0) return false;
            --balance;
        } else {
            return false;
        }
    }
    return balance == 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    string line;
    getline(cin, line);

    for (int i = 0; i < T; ++i) {
        if (!getline(cin, line)) break;

        string s = trim_codes(line);
        cout << (valid_parens(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}