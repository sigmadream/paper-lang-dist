#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    string t;
    for (char c : s) {
        if (c < 'a' || c > 'z') break;
        t += c;
    }
    string r = t;
    reverse(r.begin(), r.end());
    cout << (t == r ? "1" : "0") << "\n";
    return 0;
}