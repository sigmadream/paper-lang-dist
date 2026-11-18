#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<char> is_prime(n + 1, 1);
    is_prime[0] = 0;
    is_prime[1] = 0;

    for (int i = 2; i * i <= n; ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime[j] = 0;
            }
        }
    }

    std::string output;
    bool first = true;
    for (int x = m; x <= n; ++x) {
        if (is_prime[x]) {
            if (!first) output.push_back('\n');
            output += std::to_string(x);
            first = false;
        }
    }

    if (!first) {
        output.push_back('\n');
        std::cout << output;
    }

    return 0;
}