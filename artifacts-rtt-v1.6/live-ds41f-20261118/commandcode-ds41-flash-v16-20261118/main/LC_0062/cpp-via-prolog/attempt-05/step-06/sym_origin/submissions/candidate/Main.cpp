#include <iostream>
#include <vector>
using namespace std;

int main() {
    long long M, N;
    if (!(cin >> M >> N)) return 0;
    vector<long long> row(N, 1);
    for (long long i = 1; i < M; ++i) {
        for (long long j = 1; j < N; ++j) {
            row[j] += row[j - 1];
        }
    }
    cout << row[N - 1] << '\n';
    return 0;
}