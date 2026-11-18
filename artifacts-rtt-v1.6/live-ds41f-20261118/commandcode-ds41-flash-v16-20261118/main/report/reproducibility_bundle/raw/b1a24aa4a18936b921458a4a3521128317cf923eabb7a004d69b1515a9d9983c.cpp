#include <iostream>
#include <vector>

int main() {
    std::vector<long long> data;
    long long value;
    while (std::cin >> value) {
        data.push_back(value);
    }

    if (data.empty()) {
        return 0;
    }

    int n = static_cast<int>(data[0]);
    if (n <= 0 || data.size() < 2) {
        return 0;
    }

    long long x = data[1];
    long long cur = x;
    long long best = x;

    for (int i = 2; i <= n; ++i) {
        x = data[i];
        cur = (x > cur + x) ? x : cur + x;
        if (cur > best) {
            best = cur;
        }
    }

    std::cout << best << '\n';
    return 0;
}