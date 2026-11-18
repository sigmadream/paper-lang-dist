#include <iostream>

int n;
int full;
int ans = 0;

void dfs(int cols, int diag1, int diag2) {
    if (cols == full) {
        ++ans;
        return;
    }

    int avail = full & ~(cols | diag1 | diag2);
    while (avail) {
        int bit = avail & -avail;
        avail -= bit;
        dfs(cols | bit, ((diag1 | bit) << 1) & full, (diag2 | bit) >> 1);
    }
}

int main() {
    if (!(std::cin >> n)) {
        return 0;
    }

    full = (1 << n) - 1;
    dfs(0, 0, 0);
    std::cout << ans << '\n';

    return 0;
}