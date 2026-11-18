#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> values(n);
    for (int i = 0; i < n; ++i) cin >> values[i];

    vector<int> result;
    result.reserve(n);
    for (int x : values)
        if (x != 0) result.push_back(x);
    while ((int)result.size() < n) result.push_back(0);

    for (int i = 0; i < n; ++i) {
        if (i) cout << ' ';
        cout << result[i];
    }
    cout << '\n';
    return 0;
}