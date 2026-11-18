#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    cin >> s;
    string r = s;
    reverse(r.begin(), r.end());
    cout << (s == r ? 1 : 0) << "\n";
    return 0;
}