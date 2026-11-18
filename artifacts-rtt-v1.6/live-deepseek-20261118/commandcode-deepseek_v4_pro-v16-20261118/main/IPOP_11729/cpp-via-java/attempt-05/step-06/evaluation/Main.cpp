#include <iostream>
#include <string>

void hanoi(int n, int start, int mid, int end, std::string& out) {
    if (n == 1) {
        out += std::to_string(start) + " " + std::to_string(end) + "\n";
        return;
    }
    hanoi(n - 1, start, end, mid, out);
    out += std::to_string(start) + " " + std::to_string(end) + "\n";
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    int n;
    std::cin >> n;
    int moves = (1 << n) - 1;
    std::string output;
    output.reserve(static_cast<size_t>(moves) * 6 + 20);
    output += std::to_string(moves) + "\n";
    hanoi(n, 1, 2, 3, output);
    std::cout << output;
    return 0;
}