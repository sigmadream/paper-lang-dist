#include <iostream>
#include <string>
#include <cctype>

using namespace std;

static string trim(const string& s) {
    size_t start = 0;
    while (start < s.size() && isspace(static_cast<unsigned char>(s[start]))) {
        ++start;
    }
    size_t end = s.size();
    while (end > start && isspace(static_cast<unsigned char>(s[end - 1]))) {
        --end;
    }
    return s.substr(start, end - start);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    string dummy;
    getline(cin, dummy);

    for (int i = 0; i < T; ++i) {
        string line;
        if (!getline(cin, line)) break;

        line = trim(line);

        bool ok = true;
        int balance = 0;

        if (line.empty()) {
            ok = false;
        } else {
            for (char ch : line) {
                if (ch == '(') {
                    ++balance;
                } else if (ch == ')') {
                    if (balance > 0) {
                        --balance;
                    } else {
                        ok = false;
                        break;
                    }
                } else {
                    ok = false;
                    break;
                }
            }

            if (balance != 0) ok = false;
        }

        cout << (ok ? "YES" : "NO") << '\n';
    }

    return 0;
}