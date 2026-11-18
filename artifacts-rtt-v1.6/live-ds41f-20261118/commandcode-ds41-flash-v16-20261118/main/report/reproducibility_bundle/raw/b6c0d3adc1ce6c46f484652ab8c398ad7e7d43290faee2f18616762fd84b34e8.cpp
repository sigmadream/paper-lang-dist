#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    if (!(cin >> s >> t)) return 0;

    array<int, 26> counts{};
    for (char ch : s) {
        counts[ch - 'a']++;
    }
    for (char ch : t) {
        counts[ch - 'a']--;
    }

    bool valid = true;
    for (int c : counts) {
        if (c != 0) {
            valid = false;
            break;
        }
    }

    cout << (valid ? 1 : 0) << '\n';
    return 0;
}