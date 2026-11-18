#include <iostream>
#include <string>

void appendMove(std::string& out, int s, int e) {
    out.push_back(static_cast<char>('0' + s));
    out.push_back(' ');
    out.push_back(static_cast<char>('0' + e));
    out.push_back('\n');
}

void hanoi(int n, int s, int m, int e, std::string& out) {
    if (n == 1) {
        appendMove(out, s, e);
        return;
    }
    hanoi(n - 1, s, e, m, out);
    appendMove(out, s, e);
    hanoi(n - 1, m, s, e, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N;
    if (!(std::cin >> N)) return 0;

    long long moves = (1LL << N) - 1;

    std::string out;
    out.reserve(static_cast<size_t>(moves) * 4 + 32);

    out += std::to_string(moves);
    out.push_back('\n');

    hanoi(N, 1, 2, 3, out);

    std::cout << out;
    return 0;
}