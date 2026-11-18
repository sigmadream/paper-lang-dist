#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) {
        return 0;
    }

    int capacity = n > 0 ? static_cast<int>(n) : 0;
    std::vector<long long> a(capacity);
    int size = 0;

    while (size < capacity && (std::cin >> a[size])) {
        ++size;
    }

    int write = 0;
    for (int read = 0; read < size; ++read) {
        if (a[read] != 0) {
            long long tmp = a[write];
            a[write] = a[read];
            a[read] = tmp;
            ++write;
        }
    }

    for (int i = 0; i < size; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << a[i];
    }
    std::cout << '\n';

    return 0;
}