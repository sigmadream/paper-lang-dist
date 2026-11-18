#include <bits/stdc++.h>
using namespace std;

static string trim(const string& s) {
    size_t start = 0;
    while (start < s.size() && static_cast<unsigned char>(s[start]) <= ' ') {
        ++start;
    }
    size_t end = s.size();
    while (end > start && static_cast<unsigned char>(s[end - 1]) <= ' ') {
        --end;
    }
    return s.substr(start, end - start);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    int t = stoi(trim(first));
    string output;

    for (int i = 0; i < t; ++i) {
        string s;
        if (!getline(cin, s)) s = "";
        s = trim(s);

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
        output += valid ? "YES\n" : "NO\n";
    }

    cout << output;
    return 0;
}