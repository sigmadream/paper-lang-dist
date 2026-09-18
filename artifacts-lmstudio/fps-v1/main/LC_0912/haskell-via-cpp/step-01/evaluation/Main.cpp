#include <iostream>
#include <vector>
#include <algorithm>

std::vector<int> merge(const std::vector<int>& xs, const std::vector<int>& ys) {
    if (xs.empty()) return ys;
    if (ys.empty()) return xs;
    if (xs.front() <= ys.front()) {
        std::vector<int> result = xs;
        result.push_back(ys.front());
        result.insert(result.end(), ys.begin() + 1, ys.end());
        return result;
    } else {
        std::vector<int> result = ys;
        result.push_back(xs.front());
        result.insert(result.end(), xs.begin() + 1, xs.end());
        return result;
    }
}

std::vector<int> mergesort(const std::vector<int>& xs) {
    if (xs.size() <= 1) return xs;
    size_t mid = xs.size() / 2;
    std::vector<int> a(xs.begin(), xs.begin() + mid);
    std::vector<int> b(xs.begin() + mid, xs.end());
    return merge(mergesort(a), mergesort(b));
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> values(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> values[i];
    }
    std::vector<int> sorted_values = mergesort(values);
    for (const auto& value : sorted_values) {
        std::cout << value << " ";
    }
    return 0;
}