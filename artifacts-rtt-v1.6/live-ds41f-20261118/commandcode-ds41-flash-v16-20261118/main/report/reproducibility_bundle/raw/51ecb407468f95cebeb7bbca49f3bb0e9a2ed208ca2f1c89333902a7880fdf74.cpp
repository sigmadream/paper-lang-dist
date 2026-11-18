#include <iostream>
#include <string>

void hanoi(int n, int start, int mid, int end, std::string& sb) {
    if (n == 1) {
        sb += std::to_string(start);
        sb += ' ';
        sb += std::to_string(end);
        sb += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid, sb);
    sb += std::to_string(start);
    sb += ' ';
    sb += std::to_string(end);
    sb += '\n';
    hanoi(n - 1, mid, start, end, sb);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::string sb;
    sb += std::to_string((1LL << n) - 1);
    sb += '\n';
    hanoi(n, 1, 2, 3, sb);

    std::cout << sb;
    return 0;
}