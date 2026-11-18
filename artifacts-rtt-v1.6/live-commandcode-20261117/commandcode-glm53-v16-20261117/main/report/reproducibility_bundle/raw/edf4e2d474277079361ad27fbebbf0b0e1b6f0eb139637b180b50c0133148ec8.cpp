#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (getline(cin, s)) {
        string t = s;
        reverse(t.begin(), t.end());
        cout << (s == t ? 1 : 0) << "\n";
    }
    return 0;
}