#include <iostream>
#include <vector>
#include <algorithm>

int max_weight(int n, std::vector<int>& ropes) {
    std::sort(ropes.begin(), ropes.end(), std::greater<int>());
    int max_weight = 0;
    for (int i = 0; i < n; ++i) {
        int current_weight = ropes[i] * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }
    return max_weight;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);

    int n;
    std::cin >> n;
    std::vector<int> ropes(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> ropes[i];
    }

    int result = max_weight(n, ropes);
    std::cout << result << std::endl;

    return 0;
}
