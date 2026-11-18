#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    size_t p = line.find_first_not_of(" \t");
    if (p == string::npos) return 0;
    long long n = stoll(line.substr(p));
    if (n < 0) n = 0;
    vector<int> arr(n + 1);
    arr[0] = 0;
    for (long long i = 1; i <= n; ++i) arr[i] = arr[i / 2] + (i % 2);
    for (long long i = 0; i <= n; ++i) {
        if (i) cout << ' ';
        cout << arr[i];
    }
    cout << '\n';
    return 0;
}