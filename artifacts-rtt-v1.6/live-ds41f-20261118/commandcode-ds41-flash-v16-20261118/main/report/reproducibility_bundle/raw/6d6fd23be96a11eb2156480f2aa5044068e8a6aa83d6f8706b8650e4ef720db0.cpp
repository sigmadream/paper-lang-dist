#include <cstdio>
#include <string>

static void appendInt(std::string &out, int x) {
    char buf[12];
    int len = 0;
    if (x == 0) {
        out.push_back('0');
        return;
    }
    while (x > 0) {
        buf[len++] = static_cast<char>('0' + (x % 10));
        x /= 10;
    }
    while (len > 0) {
        out.push_back(buf[--len]);
    }
}

static void appendMove(std::string &out, int from, int to) {
    appendInt(out, from);
    out.push_back(' ');
    appendInt(out, to);
    out.push_back('\n');
}

static void hanoi(int n, int from, int mid, int to, std::string &out) {
    if (n == 0) return;
    if (n == 1) {
        appendMove(out, from, to);
        return;
    }
    hanoi(n - 1, from, to, mid, out);
    appendMove(out, from, to);
    hanoi(n - 1, mid, from, to, out);
}

int main() {
    int n;
    if (std::scanf("%d", &n) != 1) return 0;

    int count = (1 << n) - 1;
    std::string out;
    out.reserve(static_cast<size_t>(count) * 5 + 16);

    appendInt(out, count);
    out.push_back('\n');
    hanoi(n, 1, 2, 3, out);

    std::fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}