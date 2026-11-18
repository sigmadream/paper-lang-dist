#include <iostream>
#include <string>

void hanoi(int n, int start, int mid, int end, std::string& out) {
    if (n == 1) {
        out.push_back(static_cast<char>('0' + start));
        out.push_back(' ');
        out.push_back(static_cast<char>('0' + end));
        out.push_back('\n');
        return;
    }

    hanoi(n - 1, start, end, mid, out);
    out.push_back(static_cast<char>('0' + start));
    out.push_back(' ');
    out.push_back(static_cast<char>('0' + end));
    out.push_back('\n');
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    std::string out;
    out.reserve(static_cast<std::size_t>(count) * 4 + 32);

    out += std::to_string(count);
    out.push_back('\n');

    hanoi(n, 1, 2, 3, out);

    std::cout << out;
    return 0;
}