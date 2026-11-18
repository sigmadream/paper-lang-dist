#include <iostream>
#include <string>
using namespace std;

int main() {
    string s, t;
    getline(cin, s);
    getline(cin, t);

    int counts[26] = {0};

    for (size_t i = 0; i < s.size(); i++) {
        counts[s[i] - 'a']++;
    }

    for (size_t i = 0; i < t.size(); i++) {
        counts[t[i] - 'a']--;
    }

    bool valid = true;
    for (int count : counts) {
        if (count != 0) {
            valid = false;
            break;
        }
    }

    cout << (valid ? 1 : 0) << endl;
    return 0;
}