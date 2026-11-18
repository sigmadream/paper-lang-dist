#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, c;
    std::cin >> n >> c;

    std::vector<int> houses(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> houses[i];
    }

    std::sort(houses.begin(), houses.end());

    auto canPlace = [&](int distance) {
        int count = 1;
        int prev = houses[0];

        for (int i = 1; i < n; ++i) {
            if (houses[i] - prev >= distance) {
                ++count;
                prev = houses[i];
            }
        }

        return count >= c;
    };

    int low = 1;
    int high = houses.back() - houses.front();
    int answer = 0;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (canPlace(mid)) {
            answer = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    std::cout << answer << '\n';

    return 0;
}