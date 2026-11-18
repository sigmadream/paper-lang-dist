#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> scores(n);
    for (int i = 0; i < n; ++i) {
        cin >> scores[i];
    }

    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }
    if (n == 1) {
        cout << scores[0] << '\n';
        return 0;
    }

    const int negInf = -1000000000;

    int prev2One = scores[0];
    int prev2Two = negInf;

    int currOne = scores[0] + scores[1];
    int currTwo = scores[1];

    for (int i = 2; i < n; ++i) {
        int x = scores[i];

        int nextOne = currTwo + x;
        int nextTwo = max(prev2One, prev2Two) + x;

        prev2One = currOne;
        prev2Two = currTwo;
        currOne = nextOne;
        currTwo = nextTwo;
    }

    cout << max(currOne, currTwo) << '\n';
    return 0;
}