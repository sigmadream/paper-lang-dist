#include <iostream>
#include <vector>
#include <limits>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) return 0;

    if (n <= 0) return 0;

    std::vector<long long> arr;
    arr.reserve(static_cast<size_t>(n));

    long long x;
    for (long long i = 0; i < n && (std::cin >> x); ++i) {
        arr.push_back(x);
    }

    if (arr.empty()) return 0;

    long long cur = arr[0];
    long long best = arr[0];

    for (size_t i = 1; i < arr.size(); ++i) {
        cur = std::max(arr[i], cur + arr[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}