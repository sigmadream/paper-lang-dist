#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N;
    if (!(std::cin >> N)) return 0;

    std::vector<long long> scores(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> scores[i];
    }

    long long answer;

    if (N == 1) {
        answer = scores[0];
    } else if (N == 2) {
        answer = scores[0] + scores[1];
    } else {
        long long dPrev3 = 0;
        long long dPrev2 = scores[0];
        long long dPrev1 = scores[0] + scores[1];
        long long prevScore = scores[1];

        for (int i = 2; i < N; ++i) {
            long long cur = scores[i];
            long long best = std::max(dPrev2, dPrev3 + prevScore);
            long long di = best + cur;

            dPrev3 = dPrev2;
            dPrev2 = dPrev1;
            dPrev1 = di;
            prevScore = cur;
        }

        answer = dPrev1;
    }

    std::cout << answer << '\n';
    return 0;
}