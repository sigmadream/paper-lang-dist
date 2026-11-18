#include <iostream>
#include <string>
using namespace std;

string moves;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        moves += to_string(start) + " " + to_string(end) + "\n";
        return;
    }
    hanoi(n - 1, start, end, mid);
    moves += to_string(start) + " " + to_string(end) + "\n";
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    size_t p = line.find_first_not_of(" \t\r\n");
    if (p == string::npos) return 0;
    int n = stoi(line);
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    cout << count << "\n" << moves;
    return 0;
}