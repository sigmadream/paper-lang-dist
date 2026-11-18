#include <iostream>
#include <string>
using namespace std;

bool valid(const string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            ++bal;
        } else {
            if (bal == 0) return false;
            --bal;
        }
    }
    return bal == 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;

    string s;
    for (int i = 0; i < t && cin >> s; ++i) {
        cout << (valid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}