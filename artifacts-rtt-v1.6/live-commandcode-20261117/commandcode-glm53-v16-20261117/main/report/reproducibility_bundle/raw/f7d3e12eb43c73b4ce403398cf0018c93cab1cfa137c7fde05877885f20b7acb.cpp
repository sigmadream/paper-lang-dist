#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    vector<int> counts(26, 0);
    for (char c : s) counts[c - 'a']++;
    for (char c : t) counts[c - 'a']--;
    bool ok = true;
    for (int x : counts) if (x != 0) ok = false;
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}