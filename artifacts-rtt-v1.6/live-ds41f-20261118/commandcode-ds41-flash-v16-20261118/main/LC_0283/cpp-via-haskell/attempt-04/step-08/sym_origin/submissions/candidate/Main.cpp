#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> result;
    result.reserve(n);

    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        if (x != 0) {
            result.push_back(x);
        }
    }

    result.resize(n, 0);

    for (int i = 0; i < n; ++i) {
        if (i > 0) cout << ' ';
        cout << result[i];
    }
    cout << '\n';

    return 0;
}