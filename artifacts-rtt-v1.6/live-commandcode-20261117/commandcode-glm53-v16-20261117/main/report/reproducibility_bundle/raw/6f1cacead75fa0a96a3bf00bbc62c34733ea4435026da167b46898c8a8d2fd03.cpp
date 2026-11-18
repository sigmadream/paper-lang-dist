#include <cstdio>
#include <string>

static std::string sb;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        sb += std::to_string(start) + " " + std::to_string(end) + "\n";
        return;
    }
    hanoi(n - 1, start, end, mid);
    sb += std::to_string(start) + " " + std::to_string(end) + "\n";
    hanoi(n - 1, mid, start, end);
}

int main() {
    if (scanf("%d", &n_start) != 1) return 0;
    return 0;
}