#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, c;
    if (!(std::cin >> n >> c)) return 0;

    std::vector<long long> houses(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> houses[i];
    }

    std::sort(houses.begin(), houses.end());

    long long left = 1;
    long long right = houses.back() - houses.front();
    long long ans = 0;

    while (left <= right) {
        long long mid = left + (right - left) / 2;
        int count = 1;
        long long prev = houses[0];

        for (int i = 1; i < n; ++i) {
            if (houses[i] - prev >= mid) {
                ++count;
                prev = houses[i];
            }
        }

        if (count >= c) {
            ans = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    std::cout << ans << '\n';
    return 0;
}