#include <iostream>
#include <vector>

int binarySearch(int lo, int hi, int target, const std::vector<int>& a) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return (lo == a.size() || a[lo] != target) ? -1 : lo;
}

int main() {
    int n, target;
    std::cin >> n >> target;
    std::vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i];
    }
    std::cout << binarySearch(0, n, target, a) << std::endl;
    return 0;
}