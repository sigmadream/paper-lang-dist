#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    if (!getline(cin, s)) s = "";
    if (!getline(cin, t)) t = "";
    // trim
    auto trim = [](const string& x) {
        size_t a = 0, b = x.size();
        while (a < b && isspace((unsigned char)x[a])) a++;
        while (b > a && isspace((unsigned char)x[b - 1])) b--;
        return x.substr(a, b - a);
    };
    s = trim(s);
    t = trim(t);
    array<int, 26> counts{};
    for (char c : s) counts[c - 'a']++;
    for (char c : t) counts[c - 'a']--;
    bool ok = true;
    for (int x : counts) if (x != 0) { ok = false; break; }
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}