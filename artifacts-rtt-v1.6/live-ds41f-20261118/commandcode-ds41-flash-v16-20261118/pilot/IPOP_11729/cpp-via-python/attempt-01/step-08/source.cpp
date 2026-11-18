#include <iostream>
#include <string>

using namespace std;

void hanoi(int k, int start, int mid, int end, string& output) {
    if (k == 0) return;

    hanoi(k - 1, start, end, mid, output);

    output += char('0' + start);
    output += ' ';
    output += char('0' + end);
    output += '\n';

    hanoi(k - 1, mid, start, end, output);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    string output;
    output.reserve(static_cast<size_t>(count) * 4 + 20);
    output += to_string(count);
    output += '\n';

    hanoi(n, 1, 2, 3, output);

    cout << output;
    return 0;
}