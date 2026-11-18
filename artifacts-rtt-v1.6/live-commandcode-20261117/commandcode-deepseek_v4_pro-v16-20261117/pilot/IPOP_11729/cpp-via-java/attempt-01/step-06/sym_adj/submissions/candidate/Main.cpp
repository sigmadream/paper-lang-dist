#include <iostream>
using namespace std;

void hanoi(int n, int from, int aux, int to) {
    if (n == 1) {
        cout << from << ' ' << to << '\n';
        return;
    }
    hanoi(n - 1, from, to, aux);
    cout << from << ' ' << to << '\n';
    hanoi(n - 1, aux, from, to);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }
    if (n < 1 || n > 20) {
        return 0;
    }

    unsigned long long count = (1ULL << n) - 1;
    cout << count << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}