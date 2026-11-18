#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> a(n, 0);
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> a[i])) {
            a[i] = 0;
        }
    }

    int write = 0;
    for (int read = 0; read < n; ++read) {
        if (a[read] != 0) {
            int tmp = a[write];
            a[write] = a[read];
            a[read] = tmp;
            ++write;
        }
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << a[i];
    }
    std::cout << '\n';

    return 0;
}