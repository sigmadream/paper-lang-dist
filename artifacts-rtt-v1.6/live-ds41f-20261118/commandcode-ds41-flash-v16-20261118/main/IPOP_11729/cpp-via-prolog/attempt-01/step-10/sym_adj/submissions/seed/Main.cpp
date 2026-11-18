#include <iostream>
using namespace std;

void hanoi(int n, int from, int via, int to) {
    if (n == 1) {
        cout << from << ' ' << to << '\n';
        return;
    }
    hanoi(n - 1, from, to, via);
    cout << from << ' ' << to << '\n';
    hanoi(n - 1, via, from, to);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    long long count = (1LL << N) - 1;
    cout << count << '\n';

    hanoi(N, 1, 2, 3);

    return 0;
}