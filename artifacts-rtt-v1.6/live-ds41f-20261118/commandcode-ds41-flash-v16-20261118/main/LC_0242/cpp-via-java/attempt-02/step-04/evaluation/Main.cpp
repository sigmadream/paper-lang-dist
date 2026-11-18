#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    getline(cin, s);
    getline(cin, t);

    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!t.empty() && t.back() == '\r') t.pop_back();

    array<int, 26> counts{};

    for (char c : s) {
        counts[c - 'a']++;
    }
    for (char c : t) {
        counts[c - 'a']--;
    }

    bool valid = true;
    for (int count : counts) {
        if (count != 0) {
            valid = false;
            break;
        }
    }

    cout << (valid ? 1 : 0) << '\n';

    return 0;
}