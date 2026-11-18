#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    string trimmed;
    size_t s = line.find_first_not_of(" \t\r\n");
    if (s == string::npos) return 0;
    size_t e = line.find_last_not_of(" \t\r\n");
    trimmed = line.substr(s, e - s + 1);
    if (trimmed.empty()) return 0;
    int n = stoi(trimmed);
    vector<int> counts(n + 1, 0);
    string out;
    for (int i = 0; i <= n; i++) {
        if (i > 0) counts[i] = counts[i / 2] + (i % 2);
        if (i > 0) out += ' ';
        out += to_string(counts[i]);
    }
    out += '\n';
    cout << out;
    return 0;
}