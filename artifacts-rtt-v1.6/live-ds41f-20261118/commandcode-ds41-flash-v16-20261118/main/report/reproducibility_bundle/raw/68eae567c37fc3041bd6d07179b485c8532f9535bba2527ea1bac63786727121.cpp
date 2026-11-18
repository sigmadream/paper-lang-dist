#include <iostream>
#include <string>

void hanoi(int k, int start, int mid, int end, std::string& out) {
    if (k == 1) {
        out.push_back(static_cast<char>('0' + start));
        out.push_back(' ');
        out.push_back(static_cast<char>('0' + end));
        out.push_back('\n');
        return;
    }

    hanoi(k - 1, start, end, mid, out);

    out.push_back(static_cast<char>('0' + start));
    out.push_back(' ');
    out.push_back(static_cast<char>('0' + end));
    out.push_back('\n');

    hanoi(k - 1, mid, start, end, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::string out;
    out.reserve((static_cast<size_t>(1) << n) * 4 + 32);

    hanoi(n, 1, 2, 3, out);

    std::cout << ((1LL << n) - 1) << '\n' << out;
    return 0;
}