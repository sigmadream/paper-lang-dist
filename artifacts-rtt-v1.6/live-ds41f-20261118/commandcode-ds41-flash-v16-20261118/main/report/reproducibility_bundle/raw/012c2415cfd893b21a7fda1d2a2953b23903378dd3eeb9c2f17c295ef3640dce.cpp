#include <iostream>
#include <string>

using namespace std;

static void hanoi(int n, int start, int mid, int end, string& output) {
    if (n == 1) {
        output += to_string(start);
        output += ' ';
        output += to_string(end);
        output += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid, output);
    output += to_string(start);
    output += ' ';
    output += to_string(end);
    output += '\n';
    hanoi(n - 1, mid, start, end, output);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    long long count = (1LL << n) - 1;

    string output;
    output.reserve(static_cast<size_t>(count * 8 + 32));

    output += to_string(count);
    output += '\n';

    hanoi(n, 1, 2, 3, output);

    cout << output;
    return 0;
}