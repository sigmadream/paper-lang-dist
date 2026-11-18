#include <iostream>
#include <string>
using namespace std;

static string trim(const string& s) {
    int start = 0;
    int end = (int)s.length();
    while (start < end && s[start] <= ' ') start++;
    while (end > start && s[end - 1] <= ' ') end--;
    return s.substr(start, end - start);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    int t = stoi(trim(first));
    string output;

    for (int i = 0; i < t; i++) {
        string s;
        if (!getline(cin, s)) s = "";
        s = trim(s);

        int bal = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') bal++;
            else bal--;

            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) valid = false;
        output += valid ? "YES\n" : "NO\n";
    }

    cout << output;
    return 0;
}