#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> ropes(n);
    for (int i = 0; i < n; ++i) cin >> ropes[i];

    sort(ropes.begin(), ropes.end(), greater<int>());

    int max_weight = 0;
    for (int i = 0; i < n; ++i) {
        int current_weight = ropes[i] * (i + 1);
        if (current_weight > max_weight) max_weight = current_weight;
    }

    cout << max_weight << '\n';
    return 0;
}
