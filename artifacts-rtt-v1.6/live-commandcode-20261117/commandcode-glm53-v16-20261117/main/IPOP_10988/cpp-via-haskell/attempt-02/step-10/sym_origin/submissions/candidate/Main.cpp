#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    string t;
    for (char c : line)
        if (c >= 'a' && c <= 'z') t += c;
        else break;
    string r(t.rbegin(), t.rend());
    cout << (t == r ? "1" : "0") << "\n";
    return 0;
}