#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    vector<int> result;
    result.reserve(n);
    int zeroCount = 0;

    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        if (x != 0) {
            result.push_back(x);
        } else {
            ++zeroCount;
        }
    }

    for (int i = 0; i < zeroCount; ++i) {
        result.push_back(0);
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            cout << ' ';
        }
        cout << result[i];
    }
    cout << '\n';

    return 0;
}