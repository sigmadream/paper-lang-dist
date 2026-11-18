#include <iostream>
#include <string>
#include <cstdint>

static void hanoi(int n, int s, int m, int e, std::string& out) {
    if (n == 1) {
        out.push_back(static_cast<char>('0' + s));
        out.push_back(' ');
        out.push_back(static_cast<char>('0' + e));
        out.push_back('\n');
        return;
    }

    hanoi(n - 1, s, e, m, out);

    out.push_back(static_cast<char>('0' + s));
    out.push_back(' ');
    out.push_back(static_cast<char>('0' + e));
    out.push_back('\n');

    hanoi(n - 1, m, s, e, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    unsigned long long count = (1ULL << n) - 1ULL;

    std::string out;
    out.reserve(static_cast<std::size_t>(count) * 4);

    hanoi(n, 1, 2, 3, out);

    std::cout << count << '\n' << out;
    return 0;
}