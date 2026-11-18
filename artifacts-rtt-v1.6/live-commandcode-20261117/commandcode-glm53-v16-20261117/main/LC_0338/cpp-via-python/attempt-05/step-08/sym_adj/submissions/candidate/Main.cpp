#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n = 0;
    string line;
    if (getline(cin, line)) {
        string s;
        size_t i = 0;
        while (i < line.size() && isspace((unsigned char)line[i])) i++;
        size_t j = line.size();
        while (j > i && isspace((unsigned char)line[j-1])) j--;
        s = line.substr(i, j - i);
        if (!s.empty()) n = stoll(s);
    }
    vector<long long> counts(n + 1, 0);
    for (long long i = 1; i <= n; i++) {
        counts[i] = counts[i / 2] + (i % 2);
    }
    for (size_t i = 0; i < counts.size(); i++) {
        if (i) cout << ' ';
        cout << counts[i];
    }
    cout << '\n';
    return 0;
}