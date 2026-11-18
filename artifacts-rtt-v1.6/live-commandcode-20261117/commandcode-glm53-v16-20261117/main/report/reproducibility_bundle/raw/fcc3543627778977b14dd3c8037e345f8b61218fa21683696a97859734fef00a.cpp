#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    string t;
    for (char c : s) {
        if (c != '\n' && c != '\r' && !isspace(static_cast<unsigned char>(c)))
            t += c;
    }
    string r = t;
    reverse(r.begin(), r.end());
    cout << (t == r ? 1 : 0) << "\n";
    return 0;
}