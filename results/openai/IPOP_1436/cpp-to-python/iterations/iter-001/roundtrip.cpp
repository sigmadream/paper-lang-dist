#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string data;
    if (!getline(cin, data)) return 0;
    int n = stoi(data);

    int count = 0;
    int value = 665;
    while (count < n) {
        value += 1;
        if (to_string(value).find("666") != string::npos) {
            count += 1;
        }
    }

    cout << value << '\n';
    return 0;
}
