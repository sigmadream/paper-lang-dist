#include <iostream>
using namespace std;

void hanoi(int n, int s, int m, int e) {
    if (n == 1) {
        cout << s << ' ' << e << '\n';
        return;
    }
    hanoi(n - 1, s, e, m);
    cout << s << ' ' << e << '\n';
    hanoi(n - 1, m, s, e);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    long long count = (1LL << N) - 1;
    cout << count << '\n';
    hanoi(N, 1, 2, 3);

    return 0;
}