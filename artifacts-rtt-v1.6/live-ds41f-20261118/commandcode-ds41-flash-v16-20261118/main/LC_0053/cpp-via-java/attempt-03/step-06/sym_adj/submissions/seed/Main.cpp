#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::stringstream ss;
    ss << std::cin.rdbuf();
    std::string s = ss.str();

    std::istringstream iss(s);
    long long n;
    if (!(iss >> n)) return 0;

    std::vector<long long> a(n);
    for (long long i = 0; i < n; ++i) iss >> a[i];

    long long cur = a[0];
    long long best = a[0];
    for (long long i = 1; i < n; ++i) {
        cur = std::max(a[i], cur + a[i]);
        best = std::max(best, cur);
    }

    std::cout << best << "\n";
    return 0;
}