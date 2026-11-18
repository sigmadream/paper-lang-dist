#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;
    std::vector<long long> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i];
    }
    long long cur = a[0];
    long long best = a[0];
    for (int i = 1; i < n; ++i) {
        cur = std::max(a[i], cur + a[i]);
        best = std::max(best, cur);
    }
    std::cout << best << '\n';
    return 0;
}