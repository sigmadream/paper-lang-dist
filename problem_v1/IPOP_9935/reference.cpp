#include <iostream>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string s, bomb;
    if (!(cin >> s >> bomb)) return 0;
    
    string res = "";
    int b_len = bomb.length();
    
    for (char c : s) {
        res += c;
        if (res.length() >= b_len) {
            bool match = true;
            for (int i = 0; i < b_len; i++) {
                if (res[res.length() - b_len + i] != bomb[i]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                for (int i = 0; i < b_len; i++) res.pop_back();
            }
        }
    }
    
    if (res.empty()) cout << "FRULA\n";
    else cout << res << "\n";
    return 0;
}
