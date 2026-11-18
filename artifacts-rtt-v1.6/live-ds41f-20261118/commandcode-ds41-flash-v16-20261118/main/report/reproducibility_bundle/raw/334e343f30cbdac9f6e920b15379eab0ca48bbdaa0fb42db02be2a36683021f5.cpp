#include <iostream>
#include <string>

void hanoi(int k, int start, int mid, int end, std::string& moves) {
    if (k == 1) {
        moves.push_back(static_cast<char>('0' + start));
        moves.push_back(' ');
        moves.push_back(static_cast<char>('0' + end));
        moves.push_back('\n');
        return;
    }

    hanoi(k - 1, start, end, mid, moves);
    moves.push_back(static_cast<char>('0' + start));
    moves.push_back(' ');
    moves.push_back(static_cast<char>('0' + end));
    moves.push_back('\n');
    hanoi(k - 1, mid, start, end, moves);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::string moves;
    moves.reserve(static_cast<size_t>((1 << n) - 1) * 4);

    hanoi(n, 1, 2, 3, moves);

    std::cout << ((1 << n) - 1) << '\n';
    std::cout << moves;

    return 0;
}