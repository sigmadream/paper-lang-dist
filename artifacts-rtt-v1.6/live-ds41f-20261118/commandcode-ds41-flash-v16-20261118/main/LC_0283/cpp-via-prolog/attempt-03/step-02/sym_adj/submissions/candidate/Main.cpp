#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        cout << '\n';
        return 0;
    }

    vector<int> values(n);
    for (int i = 0; i < n; ++i) {
        cin >> values[i];
    }

    bool first = true;
    for (int x : values) {
        if (x != 0) {
            if (!first) cout << ' ';
            cout << x;
            first = false;
        }
    }

    for (int x : values) {
        if (x == 0) {
            if (!first) cout << ' ';
            cout << 0;
            first = false;
        }
    }

    cout << '\n';
    return 0;
}