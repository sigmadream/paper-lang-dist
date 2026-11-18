#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!getline(cin, s)) return 0;
    string r = s;
    reverse(r.begin(), r.end());
    cout << (s == r ? 1 : 0) << "\n";
    return 0;
}