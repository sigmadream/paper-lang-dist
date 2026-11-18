#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> arr(n);
    for (int i = 0; i < n; ++i) std::cin >> arr[i];

    int write = 0;
    for (int i = 0; i < n; ++i) {
        if (arr[i] != 0) {
            arr[write++] = arr[i];
        }
    }
    while (write < n) arr[write++] = 0;

    for (int i = 0; i < n; ++i) {
        if (i) std::cout << ' ';
        std::cout << arr[i];
    }
    std::cout << '\n';
    return 0;
}