#include <cstdio>
#include <cstdlib>
#include <algorithm>

int main() {
    int n;
    if (std::scanf("%d", &n) != 1) return 0;

    int *ropes = (int *)std::malloc(sizeof(int) * n);
    if (!ropes) return 0;

    for (int i = 0; i < n; i++) {
        std::scanf("%d", &ropes[i]);
    }

    std::sort(ropes, ropes + n, [](int a, int b) { return a > b; });

    long long max_weight = 0;
    for (int i = 0; i < n; i++) {
        long long current_weight = 1LL * ropes[i] * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }

    std::printf("%lld\n", max_weight);

    std::free(ropes);
    return 0;
}
