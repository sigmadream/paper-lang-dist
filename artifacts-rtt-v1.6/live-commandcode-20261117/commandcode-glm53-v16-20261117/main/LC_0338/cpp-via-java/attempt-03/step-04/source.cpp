#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    // trim
    size_t a = line.find_first_not_of(" \t\r\n");
    if (a == string::npos) return 0;
    size_t b = line.find_last_not_of(" \t\r\n");
    int n = stoi(line.substr(a, b - a + 1));
    vector<int> counts(n + 1, 0);
    string s;
    for (int i = 0; i <= n; i++) {
        if (i > 0) counts[i] = counts[i / 2] + (i % 2);
        if (i > 0) s += ' ';
        s += to_string(counts[i]);
    }
    s += '\n';
    cout << s;
    return 0;
}