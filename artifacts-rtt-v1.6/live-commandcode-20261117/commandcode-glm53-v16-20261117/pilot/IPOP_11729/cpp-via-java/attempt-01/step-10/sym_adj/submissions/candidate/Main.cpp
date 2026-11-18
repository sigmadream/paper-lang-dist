#include <bits/stdc++.h>
using namespace std;

string out;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        out += to_string(start);
        out += ' ';
        out += to_string(end);
        out += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid);
    out += to_string(start);
    out += ' ';
    out += to_string(end);
    out += '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios_base::sync_with_stdio(false);
    string line;
    if (!getline(cin, line)) return 0;
    string trimmed;
    size_t b = line.find_first_not_of(" \t\r\n");
    if (b == string::npos) return 0;
    size_t e = line.find_last_not_of(" \t\r\n");
    trimmed = line.substr(b, e - b + 1);
    int n = stoi(trimmed);
    out += to_string((1LL << n) - 1);
    out += '\n';
    hanoi(n, 1, 2, 3);
    cout << out;
    return 0;
}