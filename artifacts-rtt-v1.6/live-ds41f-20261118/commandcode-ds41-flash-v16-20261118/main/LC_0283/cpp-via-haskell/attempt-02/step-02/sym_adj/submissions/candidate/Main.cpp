#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> arr(n);
    for (int i = 0; i < n; ++i) std::cin >> arr[i];

    std::vector<long long> result;
    result.reserve(n);

    for (int i = 0; i < n; ++i) {
        if (arr[i] != 0) result.push_back(arr[i]);
    }
    while ((int)result.size() < n) result.push_back(0);

    for (int i = 0; i < n; ++i) {
        if (i) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';
    return 0;
}