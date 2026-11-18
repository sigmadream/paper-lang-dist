#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;

    string out;
    while (t-- > 0) {
        string s;
        cin >> s;
        int bal = 0;
        bool valid = true;
        for (size_t i = 0; i < s.length(); i++) {
            if (s[i] == '(') bal++;
            else bal--;
            if (bal < 0) {
                valid = false;
                break;
            }
        }
        if (bal != 0) valid = false;
        out += valid ? "YES\n" : "NO\n";
    }
    cout << out;
    return 0;
}