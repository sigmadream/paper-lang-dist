#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        string s;
        cin >> s;
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
        cout << (valid ? "YES" : "NO") << "\n";
    }
    return 0;
}
