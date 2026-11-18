#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string ns;
    if (!(cin >> ns)) return 0;

    int n;
    try {
        n = stoi(ns);
    } catch (...) {
        return 0;
    }

    string firstToken;
    if (!(cin >> firstToken)) return 0;

    long long first;
    try {
        first = stoll(firstToken);
    } catch (...) {
        return 0;
    }

    long long cur = first;
    long long best = first;

    for (int i = 1; i < n; i++) {
        string token;
        if (!(cin >> token)) break;

        long long x;
        try {
            x = stoll(token);
        } catch (...) {
            break;
        }

        cur = max(x, cur + x);
        best = max(best, cur);
    }

    cout << best << "\n";
    return 0;
}