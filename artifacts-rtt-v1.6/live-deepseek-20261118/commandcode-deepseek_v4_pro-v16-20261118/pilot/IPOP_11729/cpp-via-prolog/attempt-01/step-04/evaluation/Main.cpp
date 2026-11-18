#include <iostream>
using namespace std;

void hanoi(int n, int from, int mid, int to) {
    if (n == 1) {
        cout << from << " " << to << "\n";
        return;
    }
    hanoi(n - 1, from, to, mid);
    cout << from << " " << to << "\n";
    hanoi(n - 1, mid, from, to);
}

int main() {
    int N;
    cin >> N;
    long long count = (1LL << N) - 1;
    cout << count << "\n";
    hanoi(N, 1, 2, 3);
    return 0;
}