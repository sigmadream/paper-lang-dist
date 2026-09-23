#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        return 0;
    }

    long long val;
    if (scanf("%lld", &val) != 1) {
        return 0;
    }

    long long cur = val;
    long long best = val;
    for (int i = 1; i < n; ++i) {
        if (scanf("%lld", &val) != 1) {
            break;
        }
        cur = (cur + val > val) ? (cur + val) : val;
        if (cur > best) {
            best = cur;
        }
    }

    printf("%lld\n", best);
    return 0;
}
