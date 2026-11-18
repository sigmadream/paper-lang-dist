#include <bits/stdc++.h>
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
    string s;
    if (!getline(cin, s)) return 0;
    string t;
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    size_t j = s.size();
    while (j > i && isspace((unsigned char)s[j-1])) j--;
    t = s.substr(i, j - i);
    if (t.empty()) return 0;
    int n = stoi(t);
    hanoi(n, 1, 2, 3);
    long long count = (1LL << n) - 1;
    cout << count << "\n" << moves;
    return 0;
}