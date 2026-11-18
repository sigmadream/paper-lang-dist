#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<int> counts(N + 1, 0);
    for (int i = 0; i <= N; ++i) {
        if (i == 0) {
            counts[i] = 0;
        } else {
            counts[i] = counts[i / 2] + (i % 2);
        }
    }

    for (int i = 0; i <= N; ++i) {
        if (i > 0) cout << ' ';
        cout << counts[i];
    }
    cout << '\n';

    return 0;
}