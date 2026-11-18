#include <iostream>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N;
    if (!(std::cin >> N)) {
        return 0;
    }

    for (int i = 0; i <= N; ++i) {
        int x = i;
        int count = 0;
        while (x > 0) {
            count += (x & 1);
            x >>= 1;
        }

        if (i > 0) {
            std::cout << ' ';
        }
        std::cout << count;
    }
    std::cout << '\n';

    return 0;
}