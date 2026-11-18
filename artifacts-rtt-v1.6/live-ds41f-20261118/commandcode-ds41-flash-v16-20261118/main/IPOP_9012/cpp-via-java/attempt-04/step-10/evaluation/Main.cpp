#include <iostream>
#include <string>

using namespace std;

static bool isWhitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f' || c == '\v';
}

static bool isEmptyOrWhitespace(const string& line) {
    for (size_t i = 0; i < line.size(); ++i) {
        if (!isWhitespace(line[i])) {
            return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    int idx = 0;
    int n = static_cast<int>(first.length());

    while (idx < n && isWhitespace(first[idx])) ++idx;

    int sign = 1;
    if (idx < n && (first[idx] == '+' || first[idx] == '-')) {
        if (first[idx] == '-') sign = -1;
        ++idx;
    }

    int val = 0;
    while (idx < n && first[idx] >= '0' && first[idx] <= '9') {
        val = val * 10 + (first[idx] - '0');
        ++idx;
    }

    int t = sign * val;
    string out;

    for (int i = 0; i < t; ++i) {
        bool found = false;
        string s;

        while (true) {
            string line;
            if (!getline(cin, line)) break;

            if (!isEmptyOrWhitespace(line)) {
                s = line;
                found = true;
                break;
            }
        }

        if (!found) break;

        int balance = 0;
        bool valid = true;

        for (size_t j = 0; j < s.length(); ++j) {
            char c = s[j];

            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                --balance;
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