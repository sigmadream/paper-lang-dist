#include <iostream>
#include <string>

using namespace std;

static string sb;

static void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        sb += to_string(start) + " " + to_string(end) + "\n";
        return;
    }
    hanoi(n - 1, start, end, mid);
    sb += to_string(start) + " " + to_string(end) + "\n";
    hanoi(n - 1, mid, start, end);
}

int main() {
    int n;
    if (!(cin >> n)) return 0;
    int moves = (1 << n) - 1;
    sb += to_string(moves) + "\n";
    hanoi(n, 1, 2, 3);
    cout << sb;
    return 0;
}