#include <bits/stdc++.h>
using namespace std;

static string check(const string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance == 0) return "NO";
            --balance;
        }
    }
    return balance == 0 ? "YES" : "NO";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> tokens;
    string token;
    while (cin >> token) tokens.push_back(token);

    if (tokens.empty()) return 0;

    int n = stoi(tokens[0]);
    int processed = 0;

    for (size_t i = 1; i < tokens.size() && processed < n; ++i, ++processed) {
        cout << check(tokens[i]) << '\n';
    }

    return 0;
}