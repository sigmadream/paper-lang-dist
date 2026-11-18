#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    int t = stoi(first);
    string out;

    for (int i = 0; i < t; i++) {
        string s;
        while (getline(cin, s)) {
            bool empty = true;
            for (char c : s) {
                if (!isspace((unsigned char)c)) { empty = false; break; }
            }
            if (!empty) break;
        }
        if (!cin && s.empty()) break;

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