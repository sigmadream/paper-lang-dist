#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int start, int mid, int end, vector<string>& out) {
    if (n == 1) {
        out.push_back(to_string(start) + " " + to_string(end));
        return;
    }
    hanoi(n - 1, start, end, mid, out);
    out.push_back(to_string(start) + " " + to_string(end));
    hanoi(n - 1, mid, start, end, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<string> out;
    out.reserve((1u << n));
    out.push_back(to_string((1LL << n) - 1));
    hanoi(n, 1, 2, 3, out);
    string result;
    for (auto& s : out) { result += s; result += '\n'; }
    cout << result;
    return 0;
}