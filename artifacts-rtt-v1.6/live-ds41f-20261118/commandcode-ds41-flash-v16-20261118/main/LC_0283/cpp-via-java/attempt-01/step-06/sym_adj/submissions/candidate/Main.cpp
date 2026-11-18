#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<long long> a;
    a.reserve(static_cast<size_t>(n > 0 ? n : 0));
    long long x;
    while (static_cast<long long>(a.size()) < n && (std::cin >> x)) {
        a.push_back(x);
    }

    long long write = 0;
    for (long long read = 0; read < static_cast<long long>(a.size()); ++read) {
        if (a[static_cast<size_t>(read)] != 0) {
            long long tmp = a[static_cast<size_t>(write)];
            a[static_cast<size_t>(write)] = a[static_cast<size_t>(read)];
            a[static_cast<size_t>(read)] = tmp;
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