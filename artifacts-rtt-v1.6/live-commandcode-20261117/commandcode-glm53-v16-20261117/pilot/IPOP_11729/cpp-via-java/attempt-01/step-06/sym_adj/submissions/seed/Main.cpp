#include <iostream>
#include <string>
using namespace std;

string out;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        out += to_string(start) + " " + to_string(end) + "\n";
        return;
    }
    hanoi(n - 1, start, end, mid);
    out += to_string(start) + " " + to_string(end) + "\n";
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    size_t b = line.find_first_not_of(" \t\r\n");
    if (b == string::npos) return 0;
    int n = stoi(line.substr(b));
    out = to_string((1LL << n) - 1) + "\n";
    hanoi(n, 1, 2, 3);
    cout << out;
    return 0;
}