#include <iostream>
#include <string>
#include <functional>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    string output;
    output.reserve(static_cast<size_t>(count) * 6 + 32);

    function<void(int, int, int, int)> hanoi = [&](int k, int start, int mid, int end) {
        if (k == 0) return;

        if (k == 1) {
            output += char('0' + start);
            output += ' ';
            output += char('0' + end);
            output += '\n';
            return;
        }

        hanoi(k - 1, start, end, mid);

        output += char('0' + start);
        output += ' ';
        output += char('0' + end);
        output += '\n';

        hanoi(k - 1, mid, start, end);
    };

    hanoi(n, 1, 2, 3);

    cout << count << '\n';
    cout << output;

    return 0;
}