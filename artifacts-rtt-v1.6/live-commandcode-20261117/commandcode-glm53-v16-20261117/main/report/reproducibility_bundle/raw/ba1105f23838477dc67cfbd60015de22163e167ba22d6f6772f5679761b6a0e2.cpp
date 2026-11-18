#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (cin >> s) {
        string r(s.rbegin(), s.rend());
        cout << (s == r ? 1 : 0) << '\n';
    }
    return 0;
}