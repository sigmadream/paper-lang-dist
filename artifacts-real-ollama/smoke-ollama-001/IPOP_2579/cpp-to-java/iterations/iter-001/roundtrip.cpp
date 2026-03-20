#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> score(n + 1);
    vector<int> dp(n + 1);

    for (int index = 1; index <= n; ++index) {
        cin >> score[index];
    }

    if (n >= 1) {
        dp[1] = score[1];
    }
    if (n >= 2) {
        dp[2] = score[1] + score[2];
    }
    for (int index = 3; index <= n; ++index) {
        dp[index] = max(dp[index - 2], dp[index - 3] + score[index - 1]) + score[index];
    }

    cout << dp[n] << endl;

    return 0;
}
