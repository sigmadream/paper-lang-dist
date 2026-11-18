#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    string output;
    output.reserve(5'000'000);
    output += to_string((1 << n) - 1);
    output += '\n';

    function<void(int, int, int, int)> hanoi = [&](int count, int start, int mid, int end) {
        if (count == 1) {
            output += to_string(start);
            output += ' ';
            output += to_string(end);
            output += '\n';
            return;
        }
        hanoi(count - 1, start, end, mid);
        output += to_string(start);
        output += ' ';
        output += to_string(end);
        output += '\n';
        hanoi(count - 1, mid, start, end);
    };

    hanoi(n, 1, 2, 3);
    cout.write(output.data(), static_cast<streamsize>(output.size()));
    return 0;
}