#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;

    size_t s = line.find_first_not_of(" \t\r\n");
    if (s == string::npos) return 0;
    size_t e = line.find_last_not_of(" \t\r\n");
    line = line.substr(s, e - s + 1);
    if (line.empty()) return 0;

    int n;
    try {
        size_t pos = 0;
        long v = stol(line, &pos);
        if (pos != line.size()) return 0;
        n = static_cast<int>(v);
    } catch (...) {
        return 0;
    }

    vector<long long> a(n, 0);
    int idx = 0;
    while (idx < n) {
        string l;
        if (!getline(cin, l)) break;
        istringstream iss(l);
        string tok;
        while (idx < n && (iss >> tok)) {
            try {
                size_t pos = 0;
                long long val = stoll(tok, &pos);
                if (pos != tok.size()) break;
                a[idx++] = val;
            } catch (...) {
                break;
            }
        }
    }

    int write = 0;
    for (int read = 0; read < n; ++read) {
        if (a[read] != 0) {
            swap(a[write], a[read]);
            ++write;
        }
    }

    string out;
    out.reserve(n * 12);
    for (int i = 0; i < n; ++i) {
        if (i > 0) out += ' ';
        out += to_string(a[i]);
    }
    out += '\n';
    cout << out;
    return 0;
}