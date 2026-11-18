#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int start, int mid, int end, ostream &out) {
    if (n == 0) return;
    hanoi(n - 1, start, end, mid, out);
    out << start << ' ' << end << '\n';
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    try {
        size_t pos;
        int n = stoi(line, &pos);
        // mimic Prolog number_codes: entire line must be a number
        while (pos < line.size() && isspace((unsigned char)line[pos])) pos++;
        if (pos != line.size()) return 0;
        if (n < 1) return 0;
        ostringstream out;
        hanoi(n, 1, 2, 3, out);
        string s = out.str();
        long long count = 0;
        for (char c : s) if (c == '\n') count++;
        cout << count << '\n' << s;
    } catch (...) {
    }
    return 0;
}