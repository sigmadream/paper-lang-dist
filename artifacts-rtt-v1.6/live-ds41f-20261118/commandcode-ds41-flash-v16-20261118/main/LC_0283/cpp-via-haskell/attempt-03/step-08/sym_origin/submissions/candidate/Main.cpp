#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;
    std::vector<int> values(n);
    for (int i = 0; i < n; ++i) std::cin >> values[i];

    std::vector<int> result;
    result.reserve(n);
    for (int x : values) if (x != 0) result.push_back(x);
    while ((int)result.size() < n) result.push_back(0);

    for (int i = 0; i < n; ++i) {
        if (i) std::cout << ' ';
        std::cout << result[i];
    }
    std::cout << '\n';
    return 0;
}