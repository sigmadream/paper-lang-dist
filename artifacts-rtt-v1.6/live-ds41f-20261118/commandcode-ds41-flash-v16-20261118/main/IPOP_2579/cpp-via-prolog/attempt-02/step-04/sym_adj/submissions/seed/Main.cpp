#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<long long> score(N + 1);
    for (int i = 1; i <= N; ++i) {
        cin >> score[i];
    }

    if (N == 1) {
        cout << score[1] << '\n';
        return 0;
    }

    if (N == 2) {
        cout << score[1] + score[2] << '\n';
        return 0;
    }

    long long dPrev3 = 0;
    long long dPrev2 = score[1];
    long long dPrev1 = score[1] + score[2];

    for (int i = 3; i <= N; ++i) {
        long long best = max(dPrev2, dPrev3 + score[i - 1]);
        long long di = best + score[i];
        dPrev3 = dPrev2;
        dPrev2 = dPrev1;
        dPrev1 = di;
    }

    cout << dPrev1 << '\n';
    return 0;
}