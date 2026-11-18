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
    int n;
    cin >> n;
    long long total = (1LL << n) - 1;
    cout << total << '\n';
    hanoi(n, 1, 2, 3);
    return 0;
}