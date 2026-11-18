#include <cstdio>
#include <string>
#include <functional>

static void hanoi(int n, int s, int m, int e, std::string& out) {
    if (n == 1) {
        out += static_cast<char>('0' + s);
        out += ' ';
        out += static_cast<char>('0' + e);
        out += '\n';
        return;
    }
    hanoi(n - 1, s, e, m, out);
    out += static_cast<char>('0' + s);
    out += ' ';
    out += static_cast<char>('0' + e);
    out += '\n';
    hanoi(n - 1, m, s, e, out);
}

int main() {
    int N;
    if (std::scanf("%d", &N) != 1) return 0;

    long long count = (1LL << N) - 1;

    std::string out;
    out.reserve(static_cast<size_t>(count) * 4 + 32);
    out += std::to_string(count);
    out += '\n';

    hanoi(N, 1, 2, 3, out);

    std::fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}