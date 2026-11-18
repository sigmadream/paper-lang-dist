#include <bits/stdc++.h>
using namespace std;

static string trim_string(const string& s) {
    size_t a = 0, b = s.size();
    while (a < b) {
        unsigned char c = static_cast<unsigned char>(s[a]);
        if (c == 9 || c == 10 || c == 11 || c == 12 || c == 13 || c == 32) ++a;
        else break;
    }
    while (b > a) {
        unsigned char c = static_cast<unsigned char>(s[b - 1]);
        if (c == 9 || c == 10 || c == 11 || c == 12 || c == 13 || c == 32) --b;
        else break;
    }
    return s.substr(a, b - a);
}

static bool valid_parens(const string& s) {
    if (s.empty()) return false;
    int bal = 0;
    for (char ch : s) {
        if (ch == '(') {
            ++bal;
        } else if (ch == ')') {
            if (bal <= 0) return false;
            --bal;
        } else {
            return false;
        }
    }
    return bal == 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    string tstr = trim_string(first);
    if (tstr.empty()) return 0;

    int T = 0;
    try {
        T = stoi(tstr);
    } catch (...) {
        return 0;
    }

    for (int i = 0; i < T; ++i) {
        string line;
        if (!getline(cin, line)) break;

        string s = trim_string(line);
        cout << (valid_parens(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}