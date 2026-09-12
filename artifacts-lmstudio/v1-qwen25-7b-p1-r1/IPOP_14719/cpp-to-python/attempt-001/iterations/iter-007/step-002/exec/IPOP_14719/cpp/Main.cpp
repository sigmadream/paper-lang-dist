#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);

    int h, w;
    std::cin >> h >> w;
    std::vector<int> a(w);
    for (int i = 0; i < w; ++i) {
        std::cin >> a[i];
    }

    int ans = 0;
    for (int i = 1; i < w - 1; ++i) {
        int left_max = *std::max_element(a.begin(), a.begin() + i + 1);
        int right_max = *std::max_element(a.begin() + i, a.end());
        int bound = std::min(left_max, right_max);
        if (bound > a[i]) {
            ans += bound - a[i];
        }
    }

    std::cout << ans << std::endl;

    return 0;
}
