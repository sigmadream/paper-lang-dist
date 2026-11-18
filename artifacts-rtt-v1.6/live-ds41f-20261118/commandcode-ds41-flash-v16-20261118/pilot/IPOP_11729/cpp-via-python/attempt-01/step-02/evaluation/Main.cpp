#include <bits/stdc++.h>
using namespace std;

static string output_buffer;

void hanoi(int k, int start, int mid, int end) {
    if (k == 0) return;
    if (k == 1) {
        output_buffer.push_back(char('0' + start));
        output_buffer.push_back(' ');
        output_buffer.push_back(char('0' + end));
        output_buffer.push_back('\n');
        return;
    }

    hanoi(k - 1, start, end, mid);

    output_buffer.push_back(char('0' + start));
    output_buffer.push_back(' ');
    output_buffer.push_back(char('0' + end));
    output_buffer.push_back('\n');

    hanoi(k - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long moves = (1LL << n) - 1;

    output_buffer.reserve(static_cast<size_t>(moves) * 4 + 32);
    output_buffer += to_string(moves);
    output_buffer.push_back('\n');

    hanoi(n, 1, 2, 3);

    cout << output_buffer;
    return 0;
}