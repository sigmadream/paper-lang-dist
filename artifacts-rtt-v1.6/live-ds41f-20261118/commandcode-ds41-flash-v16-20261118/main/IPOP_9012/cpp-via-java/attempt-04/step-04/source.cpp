#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    int idx = 0;
    int n = (int)first.length();
    while (idx < n && isspace((unsigned char)first[idx])) idx++;

    int sign = 1;
    if (idx < n && (first[idx] == '+' || first[idx] == '-')) {
        if (first[idx] == '-') sign = -1;
        idx++;
    }

    int val = 0;
    while (idx < n && isdigit((unsigned char)first[idx])) {
        val = val * 10 + (first[idx] - '0');
        idx++;
    }

    int t = sign * val;
    string out;

    for (int i = 0; i < t; i++) {
        string s;
        bool found = false;

        while (true) {
            string line;
            if (!getline(cin, line)) break;

            bool empty = true;
            for (int j = 0; j < (int)line.length(); j++) {
                if (!isspace((unsigned char)line[j])) {
                    empty = false;
                    break;
                }
            }

            if (!empty) {
                s = line;
                found = true;
                break;
            }
        }

        if (!found) break;

        int balance = 0;
        bool valid = true;

        for (int j = 0; j < (int)s.length(); j++) {
            char c = s[j];
            if (c == '(') {
                balance++;
            } else if (c == ')') {
                balance--;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) {
            valid = false;
        }

        out += valid ? "YES\n" : "NO\n";
    }

    cout << out;
    return 0;
}