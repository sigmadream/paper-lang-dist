#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> a(static_cast<size_t>(n), 0);
    for (long long i = 0; i < n; ++i) {
        if (!(std::cin >> a[static_cast<size_t>(i)])) break;
    }

    size_t write = 0;
    for (size_t read = 0; read < a.size(); ++read) {
        if (a[read] != 0) {
            std::swap(a[write], a[read]);
            ++write;
        }
    }

    for (size_t i = 0; i < a.size(); ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << a[i];
    }
    std::cout << '\n';

    return 0;
}