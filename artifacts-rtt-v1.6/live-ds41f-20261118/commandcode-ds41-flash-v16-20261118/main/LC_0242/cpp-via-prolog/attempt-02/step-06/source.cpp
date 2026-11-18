#include <bits/stdc++.h>
using namespace std;

int main() {
    string s, t;
    if (!getline(cin, s)) s = "";
    if (!getline(cin, t)) t = "";

    auto clean = [](string &x) {
        string r;
        for (char c : x) {
            if (!(c == 32 || c == 9 || c == 10 || c == 13)) r += c;
        }
        x = r;
    };

    clean(s);
    clean(t);

    sort(s.begin(), s.end());
    sort(t.begin(), t.end());

    cout << (s == t ? 1 : 0) << '\n';
    return 0;
}