#include <iostream>
#include <string>

using namespace std;

string output;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        output += to_string(start);
        output += ' ';
        output += to_string(end);
        output += '\n';
        return;
    }

    hanoi(n - 1, start, end, mid);
    output += to_string(start);
    output += ' ';
    output += to_string(end);
    output += '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    output += to_string(count);
    output += '\n';

    hanoi(n, 1, 2, 3);

    cout << output;
    return 0;
}