#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>
#include <climits>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> values;
    values.reserve(n);
    for (long long i = 0; i < n; ++i) {
        long long x;
        std::cin >> x;
        values.push_back(x);
    }

    if (values.empty()) return 0;

    long long cur = values[0];
    long long best = values[0];
    for (size_t i = 1; i < values.size(); ++i) {
        cur = std::max(values[i], cur + values[i]);
        best = std::max(best, cur);
    }

    std::cout << best << "\n";
    return 0;
}