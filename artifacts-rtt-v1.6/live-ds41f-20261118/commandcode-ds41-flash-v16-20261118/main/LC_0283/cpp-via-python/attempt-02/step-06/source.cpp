#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> a;
    a.reserve(static_cast<size_t>(n));
    long long x;
    while (static_cast<long long>(a.size()) < n && (std::cin >> x)) {
        a.push_back(x);
    }

    size_t write = 0;
    for (size_t read = 0; read < a.size(); ++read) {
        if (a[read] != 0) {
            std::swap(a[write], a[read]);
            ++write;
        }
    }

    for (size_t i = 0; i < a.size(); ++i) {
        if (i) std::cout << ' ';
        std::cout << a[i];
    }
    std::cout << '\n';

    return 0;
}