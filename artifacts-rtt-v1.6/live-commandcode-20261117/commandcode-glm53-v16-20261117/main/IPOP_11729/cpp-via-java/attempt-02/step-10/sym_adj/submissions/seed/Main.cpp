#include <iostream>
#include <string>
#include <sstream>
using namespace std;

static string moves;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        moves += to_string(start);
        moves += ' ';
        moves += to_string(end);
        moves += '\n';
        return;
    }
    hanoi(n - 1, start, end, mid);
    moves += to_string(start);
    moves += ' ';
    moves += to_string(end);
    moves += '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    string s;
    if (!getline(cin, s)) return 0;
    string t;
    {
        size_t a = s.find_first_not_of(" \t\r\n");
        if (a == string::npos) return 0;
        size_t b = s.find_last_not_of(" \t\r\n");
        t = s.substr(a, b - a + 1);
    }
    if (t.empty()) return 0;
    int n;
    istringstream iss(t);
    if (!(iss >> n)) return 0;
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    cout << count << '\n' << moves;
    return 0;
}