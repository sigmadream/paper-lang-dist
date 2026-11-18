#include <iostream>
#include <string>
#include <cctype>

using namespace std;

static bool isWhitespace(char c) {
    return isspace(static_cast<unsigned char>(c)) != 0;
}

static bool isEmptyOrWhitespace(const string& line) {
    for (size_t i = 0; i < line.length(); i++) {
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

    size_t idx = 0;
    size_t n = first.length();

    while (idx < n && isWhitespace(first[idx])) idx++;

    int sign = 1;
    if (idx < n && (first[idx] == '+' || first[idx] == '-')) {
        if (first[idx] == '-') sign = -1;
        idx++;
    }

    int val = 0;
    while (idx < n && isdigit(static_cast<unsigned char>(first[idx]))) {
        val = val * 10 + (first[idx] - '0');
        idx++;
    }

    int t = sign * val;
    string out;

    for (int i = 0; i < t; i++) {
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

        for (size_t j = 0; j < s.length(); j++) {
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