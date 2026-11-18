#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    // parse first token as integer
    long long n = 0;
    bool neg = false;
    size_t i = 0;
    while (i < line.size() && isspace((unsigned char)line[i])) i++;
    bool valid = false;
    if (i < line.size() && (line[i] == '-' || line[i] == '+')) {
        if (line[i] == '-') neg = true;
        i++;
    }
    if (i < line.size() && isdigit((unsigned char)line[i])) {
        valid = true;
        for (; i < line.size() && isdigit((unsigned char)line[i]); i++) {
            n = n * 10 + (line[i] - '0');
        }
    }
    if (!valid) n = 0;
    if (neg) n = -n;
    if (n < 0) n = 0;
    if (n > 100000) n = 100000;

    vector<int> counts(n + 1);
    counts[0] = 0;
    for (long long k = 1; k <= n; k++) {
        counts[k] = counts[k / 2] + (int)(k % 2);
    }
    for (long long k = 0; k <= n; k++) {
        if (k) cout << ' ';
        cout << counts[k];
    }
    cout << '\n';
    return 0;
}