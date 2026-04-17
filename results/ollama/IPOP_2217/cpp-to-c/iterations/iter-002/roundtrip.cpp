#include <iostream>
#include <vector>
#include <algorithm>

int compare(const void *a, const void *b) {
    return (*(int*)b - *(int*)a);
}

int main() {
    int n;
    std::cin >> n;

    std::vector<int> ropes(n);
    for (int i = 0; i < n; i++) {
        std::cin >> ropes[i];
    }

    qsort(ropes.data(), n, sizeof(int), compare);

    long long max_weight = 0;
    for (int i = 0; i < n; i++) {
        long long current_weight = static_cast<long long>(ropes[i]) * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }

    std::cout << max_weight << std::endl;
    return 0;
}
