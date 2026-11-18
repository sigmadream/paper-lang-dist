#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> arr(n);
    for (int i = 0; i < n; ++i) cin >> arr[i];

    vector<int> nonZeros;
    vector<int> zeros;
    nonZeros.reserve(n);
    zeros.reserve(n);

    for (int x : arr) {
        if (x == 0) zeros.push_back(x);
        else nonZeros.push_back(x);
    }

    bool first = true;
    for (int x : nonZeros) {
        if (!first) cout << ' ';
        cout << x;
        first = false;
    }
    for (int x : zeros) {
        if (!first) cout << ' ';
        cout << x;
        first = false;
    }
    cout << '\n';

    return 0;
}