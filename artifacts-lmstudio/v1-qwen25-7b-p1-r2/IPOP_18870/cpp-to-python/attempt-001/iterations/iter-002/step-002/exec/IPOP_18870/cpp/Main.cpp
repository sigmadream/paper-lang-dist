#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <sstream>

std::vector<int> coordinate_compression(int n, const std::vector<int>& a) {
    std::set<int> sorted_a(a.begin(), a.end());
    std::vector<int> compressed;
    std::unordered_map<int, int> index_map;

    int index = 0;
    for (const auto& x : sorted_a) {
        index_map[x] = index++;
    }

    for (const auto& x : a) {
        compressed.push_back(index_map[x]);
    }

    return compressed;
}

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

    std::vector<int> result = coordinate_compression(n, a);
    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << " ";
        std::cout << result[i];
    }
    std::cout << std::endl;

    return 0;
}
