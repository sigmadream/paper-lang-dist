#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    int t = stoi(line);
    while (t-- > 0) {
        if (!getline(cin, line)) break;
        int b = 0;
        bool ok = true;
        for (char c : line) {
            b += (c == '(') ? 1 : -1;
            if (b < 0) { ok = false; break; }
        }
        cout << ((ok && b == 0) ? "YES" : "NO") << "\n";
    }
    return 0;
}