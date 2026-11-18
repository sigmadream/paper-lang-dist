#include <iostream>
#include <string>
#include <cstdlib>

static void hanoi(int n, int start, int mid, int end, std::string& out) {
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

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    int n = std::atoi(line.c_str());
    int moves = (1 << n) - 1;

    std::string out;
    out.reserve(static_cast<size_t>(4) * moves + 16);

    out.append(std::to_string(moves));
    out.push_back('\n');

    hanoi(n, 1, 2, 3, out);

    std::cout << out;
    return 0;
}