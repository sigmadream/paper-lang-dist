#include <iostream>
#include <string>
using namespace std;

static string sb;

static void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        sb.push_back(char('0' + start));
        sb.push_back(' ');
        sb.push_back(char('0' + end));
        sb.push_back('\n');
        return;
    }
    hanoi(n - 1, start, end, mid);
    sb.push_back(char('0' + start));
    sb.push_back(' ');
    sb.push_back(char('0' + end));
    sb.push_back('\n');
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long count = (1LL << n) - 1;

    sb.reserve(20 * 1048575 + 32);
    sb.append(to_string(count));
    sb.push_back('\n');
    hanoi(n, 1, 2, 3);

    cout << sb;
    return 0;
}