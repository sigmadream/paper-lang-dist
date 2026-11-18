#include <iostream>

int main() {
    long long M, N;
    if (!(std::cin >> M >> N)) {
        return 0;
    }

    std::vector<long long> row(N, 1);
    for (long long i = 1; i < M; ++i) {
        for (long long j = 1; j < N; ++j) {
            row[j] += row[j - 1];
        }
    }

    std::cout << row[N - 1] << '\n';
    return 0;
}