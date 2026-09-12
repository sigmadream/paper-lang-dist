#include <iostream>
#include <vector>
#include <set>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);

    int n;
    std::cin >> n;
    std::vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i];
    }

    std::set<int> sorted_a(a.begin(), a.end());
    std::vector<int> compressed;
    for (const auto& x : sorted_a) {
        compressed.push_back(x);
    }

    for (int i = 0; i < n; ++i) {
        auto it = std::lower_bound(compressed.begin(), compressed.end(), a[i]);
        std::cout << std::distance(compressed.begin(), it) << " ";
    }
    std::cout << std::endl;

    return 0;
}
