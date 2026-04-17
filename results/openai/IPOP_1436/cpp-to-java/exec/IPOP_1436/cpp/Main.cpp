#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    int count = 0;
    int value = 665;
    while (count < n) {
        ++value;
        if (to_string(value).find("666") != string::npos) {
            ++count;
        }
    }

    cout << value;
    return 0;
}
