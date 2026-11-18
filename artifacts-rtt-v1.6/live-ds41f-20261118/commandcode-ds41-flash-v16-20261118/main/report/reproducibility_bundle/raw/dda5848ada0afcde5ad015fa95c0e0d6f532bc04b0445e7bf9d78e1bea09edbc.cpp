#include <bits/stdc++.h>
using namespace std;

bool isCWhitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' ||
           c == '\v' || c == '\f' || c == '\r';
}

string stripTrailing(string s) {
    while (!s.empty() && isCWhitespace(s.back())) {
        s.pop_back();
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> lines;
    string line;
    while (getline(cin, line)) {
        lines.push_back(line);
    }

    if (lines.empty()) {
        return 0;
    }

    if (lines.size() == 1) {
        cout << "0\n";
        return 0;
    }

    string s = stripTrailing(lines[0]);
    string t = stripTrailing(lines[1]);

    sort(s.begin(), s.end());
    sort(t.begin(), t.end());

    cout << (s == t ? "1\n" : "0\n");
    return 0;
}