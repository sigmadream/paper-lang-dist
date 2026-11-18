#include <iostream>
#include <string>
using namespace std;

string sb;

void hanoi(int n, int start, int mid, int end) {
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
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    cout << count << "\n" << sb;
    return 0;
}