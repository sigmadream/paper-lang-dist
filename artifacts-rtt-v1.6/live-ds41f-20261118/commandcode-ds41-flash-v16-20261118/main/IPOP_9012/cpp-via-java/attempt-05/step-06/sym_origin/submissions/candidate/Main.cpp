#include <bits/stdc++.h>
using namespace std;

static string trimStr(const string& s) {
    size_t b = 0, e = s.size();
    while (b < e && isspace((unsigned char)s[b])) ++b;
    while (e > b && isspace((unsigned char)s[e - 1])) --e;
    return s.substr(b, e - b);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    int t = stoi(trimStr(first));
    string output;

    for (int i = 0; i < t; ++i) {
        string s;
        if (!getline(cin, s)) s = "";
        s = trimStr(s);

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else {
                --balance;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) valid = false;

        output += valid ? "YES\n" : "NO\n";
    }

    cout << output;
    return 0;
}