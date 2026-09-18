#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;
    std::vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> arr[i];
    }
    std::sort(arr.begin(), arr.end());
    for (int i = 0; i < n; ++i) {
        if (i > 0) std::cout << " ";
        std::cout << arr[i];
    }
    std::cout << std::endl;
    return 0;
}