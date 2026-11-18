#include <iostream>
#include <string>
using namespace std;

string sb;

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        sb += to_string(start) + ' ' + to_string(end) + '\n';
        return;
    }
    hanoi(n - 1, start, end, mid);
    sb += to_string(start) + ' ' + to_string(end) + '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    if (!getline(cin, s)) return 0;
    string t;
    size_t a = s.find_first_not_of(" \t\r\n");
    if (a == string::npos) return 0;
    size_t b = s.find_last_not_of(" \t\r\n");
    t = s.substr(a, b - a + 1);
    int n = stoi(t);
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    cout << count << '\n' << sb;
}