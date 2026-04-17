#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    std::cin >> n;

    std::vector<int> ropes(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> ropes[i];
    }

    std::sort(ropes.begin(), ropes.end(), std::greater<int>());

    int max_weight = 0;
    for (int i = 0; i < n; ++i) {
        int current_weight = ropes[i] * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }

    std::cout << max_weight << std::endl;

    return 0;
}
