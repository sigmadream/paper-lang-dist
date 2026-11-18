#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N, C;
    if (!(std::cin >> N >> C)) return 0;

    std::vector<long long> houses(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> houses[i];
    }

    std::sort(houses.begin(), houses.end());

    auto countInstall = [&](long long distance) {
        int count = 1;
        long long prev = houses[0];
        for (int i = 1; i < N; ++i) {
            if (houses[i] - prev >= distance) {
                ++count;
                prev = houses[i];
            }
        }
        return count;
    };

    long long left = 1;
    long long right = houses.back() - houses.front();
    long long answer = 0;

    while (left <= right) {
        long long mid = left + (right - left) / 2;
        if (countInstall(mid) >= C) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    std::cout << answer << '\n';
    return 0;
}