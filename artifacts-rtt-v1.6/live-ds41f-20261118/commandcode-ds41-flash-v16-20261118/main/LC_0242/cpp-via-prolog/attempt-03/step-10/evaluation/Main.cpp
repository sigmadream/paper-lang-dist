#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    getline(cin, s);
    getline(cin, t);

    // Remove trailing carriage returns if present
    if (!s.empty() && s.back() == '\r') s.pop_back();
    if (!t.empty() && t.back() == '\r') t.pop_back();

    bool ok = (s.size() == t.size());
    if (ok) {
        int cnt[26] = {0};
        for (char c : s) cnt[c - 'a']++;
        for (char c : t) cnt[c - 'a']--;
        for (int i = 0; i < 26; i++) {
            if (cnt[i] != 0) {
                ok = false;
                break;
            }
        }
    }

    cout << (ok ? 1 : 0) << '\n';
    return 0;
}