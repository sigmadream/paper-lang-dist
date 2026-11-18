#include <bits/stdc++.h>
using namespace std;

static string output;

static void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        output.push_back(char('0' + start));
        output.push_back(' ');
        output.push_back(char('0' + end));
        output.push_back('\n');
        return;
    }

    hanoi(n - 1, start, end, mid);
    output.push_back(char('0' + start));
    output.push_back(' ');
    output.push_back(char('0' + end));
    output.push_back('\n');
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    long long count = (1LL << n) - 1;

    output.reserve(static_cast<size_t>(count) * 4);
    output.append(to_string(count));
    output.push_back('\n');

    hanoi(n, 1, 2, 3);

    cout << output;
    return 0;
}