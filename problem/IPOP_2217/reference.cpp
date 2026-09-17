#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> ropes(n);
    for (int i = 0; i < n; i++) {
        cin >> ropes[i];
    }

    sort(ropes.begin(), ropes.end(), greater<int>());

    long long max_weight = 0;
    for (int i = 0; i < n; i++) {
        long long current_weight = 1LL * ropes[i] * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }

    cout << max_weight << "\n";
    return 0;
}
