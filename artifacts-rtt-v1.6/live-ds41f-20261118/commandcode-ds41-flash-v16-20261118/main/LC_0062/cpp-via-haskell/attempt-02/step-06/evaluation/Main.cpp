#include <iostream>
#include <algorithm>
using namespace std;

void printInt128(__int128 x) {
    if (x == 0) { cout << 0; return; }
    if (x < 0) { cout << '-'; x = -x; }
    string s;
    while (x > 0) {
        s.push_back('0' + (int)(x % 10));
        x /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s;
}

int main() {
    long long m, n;
    if (!(cin >> m >> n)) return 0;
    long long k = min(m - 1, n - 1);
    long long r = m + n - 2;
    __int128 num = 1, den = 1;
    for (long long i = 1; i <= k; ++i) {
        num *= (__int128)(r - k + i);
        den *= (__int128)i;
    }
    __int128 ans = num / den;
    printInt128(ans);
    cout << '\n';
    return 0;
}