#include <bits/stdc++.h>
using namespace std;

string moves;

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
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    if (!getline(cin, s)) return 0;
    string t;
    size_t i = 0, j = s.size();
    while (i < j && isspace((unsigned char)s[i])) i++;
    while (j > i && isspace((unsigned char)s[j - 1])) j--;
    t = s.substr(i, j - i);
    if (t.empty()) return 0;
    try {
        int n = stoi(t);
        hanoi(n, 1, 2, 3);
        long long count = (1LL << n) - 1;
        cout << count << '\n' << moves;
    } catch (...) {
        return 0;
    }
    return 0;
}