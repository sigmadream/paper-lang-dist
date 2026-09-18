#include <iostream>
#include <vector>

int search(const std::vector<int>& array, int target, int lo, int hi) {
    if (lo > hi) return -1;
    int mid = (lo + hi) / 2;
    if (array[mid] == target) return mid;
    else if (array[mid] < target) return search(array, target, mid + 1, hi);
    else return search(array, target, lo, mid - 1);
}

int main() {
    int n, target;
    std::cin >> n >> target;
    std::vector<int> xs(n);
    for (int i = 0; i < n; ++i) std::cin >> xs[i];
    std::cout << search(xs, target, 0, n - 1) << std::endl;
    return 0;
}