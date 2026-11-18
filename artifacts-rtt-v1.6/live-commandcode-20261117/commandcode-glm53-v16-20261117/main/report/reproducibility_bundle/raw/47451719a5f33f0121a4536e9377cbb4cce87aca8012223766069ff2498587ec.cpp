#include <iostream>
#include <string>
using namespace std;

string out;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        out += to_string(start) + ' ' + to_string(end) + '\n';
        return;
    }
    hanoi(n - 1, start, end, mid);
    out += to_string(start) + ' ' + to_string(end) + '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    size_t pos = line.find_first_not_of(" \t\r\n");
    if (pos == string::npos) return 0;
    int n = stoi(line.substr(pos));
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    string sb = to_string(count) + '\n' + out;
    cout << sb;
    return 0;
}