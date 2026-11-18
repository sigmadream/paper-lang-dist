#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    string t;
    for (char c : line) {
        if (islower((unsigned char)c)) t += c;
        else break;
    }
    string r = t;
    reverse(r.begin(), r.end());
    cout << (t == r ? "1" : "0") << "\n";
    return 0;
}