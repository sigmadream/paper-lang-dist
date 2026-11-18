#include <iostream>
#include <string>

using namespace std;

void hanoi(int n, int from, int aux, int to, string& sb) {
    if (n == 1) {
        sb += to_string(from) + " " + to_string(to) + "\n";
        return;
    }
    hanoi(n - 1, from, to, aux, sb);
    sb += to_string(from) + " " + to_string(to) + "\n";
    hanoi(n - 1, aux, from, to, sb);
}

int main() {
    int n;
    cin >> n;
    int moves = (1 << n) - 1;
    string sb;
    sb += to_string(moves);
    sb += "\n";
    hanoi(n, 1, 2, 3, sb);
    cout << sb;
    return 0;
}