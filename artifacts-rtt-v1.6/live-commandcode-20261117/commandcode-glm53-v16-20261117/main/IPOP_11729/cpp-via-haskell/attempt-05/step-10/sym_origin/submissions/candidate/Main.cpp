#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e) {
    if (n == 1) { cout << s << ' ' << e << '\n'; return; }
    hanoi(n - 1, s, e, m);
    cout << s << ' ' << e << '\n';
    hanoi(n - 1, m, s, e);
}

int main() {
    string s;
    if (!getline(cin, s)) return 0;
    size_t i = 0;
    while (i < s.size() && !isdigit((unsigned char)s[i])) i++;
    size_t j = i;
    while (j < s.size() && isdigit((unsigned char)s[j])) j++;
    long long n = (i < j) ? stoll(s.substr(i, j - i)) : 0;
    cout << ((1LL << n) - 1) << '\n';
    if (n > 0) hanoi((int)n, 1, 2, 3);
    return 0;
}