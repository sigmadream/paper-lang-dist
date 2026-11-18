#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;

    vector<int> nonZeros;
    int zeroCount = 0;

    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        if (x == 0) {
            ++zeroCount;
        } else {
            nonZeros.push_back(x);
        }
    }

    bool first = true;
    for (int x : nonZeros) {
        if (!first) cout << ' ';
        cout << x;
        first = false;
    }

    for (int i = 0; i < zeroCount; ++i) {
        if (!first) cout << ' ';
        cout << 0;
        first = false;
    }

    cout << '\n';
    return 0;
}