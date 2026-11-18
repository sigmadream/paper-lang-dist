#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, c;
    std::cin >> n >> c;

    std::vector<int> homes(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> homes[i];
    }

    std::sort(homes.begin(), homes.end());

    auto countPlacements = [&](int d) {
        int count = 1;
        int prev = homes[0];

        for (int i = 1; i < n; ++i) {
            if (homes[i] - prev >= d) {
                ++count;
                prev = homes[i];
            }
        }

        return count;
    };

    int left = 1;
    int right = homes.back() - homes.front();
    int answer = 0;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (countPlacements(mid) >= c) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    std::cout << answer << '\n';
    return 0;
}