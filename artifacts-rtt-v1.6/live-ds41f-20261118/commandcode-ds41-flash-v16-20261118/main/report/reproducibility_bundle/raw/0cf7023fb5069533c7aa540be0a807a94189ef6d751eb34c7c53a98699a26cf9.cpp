#include <iostream>
#include <string>

using namespace std;

static bool isSpace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' ||
           c == '\f' || c == '\v';
}

static string trimStr(const string& s) {
    size_t b = 0;
    size_t e = s.length();

    while (b < e && isSpace(s[b])) {
        ++b;
    }
    while (e > b && isSpace(s[e - 1])) {
        --e;
    }

    return s.substr(b, e - b);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) {
        return 0;
    }

    int t = stoi(trimStr(first));
    string output;

    for (int i = 0; i < t; ++i) {
        string s;
        if (!getline(cin, s)) {
            s = "";
        } else {
            s = trimStr(s);
        }

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else {
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

        output += valid ? "YES\n" : "NO\n";
    }

    cout << output;
    return 0;
}