#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> arr[i];
    }

    if (n == 0) {
        std::cout << 0 << '\n';
        return 0;
    }

    int best = arr[0];
    int cur = arr[0];

    for (int i = 1; i < n; ++i) {
        cur = std::max(arr[i], cur + arr[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}