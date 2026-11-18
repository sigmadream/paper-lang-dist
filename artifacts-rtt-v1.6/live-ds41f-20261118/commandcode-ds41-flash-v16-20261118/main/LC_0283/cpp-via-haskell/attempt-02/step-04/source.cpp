#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }

    vector<long long> result;
    result.reserve(n);

    for (int i = 0; i < n; ++i) {
        if (nums[i] != 0) {
            result.push_back(nums[i]);
        }
    }

    while ((int)result.size() < n) {
        result.push_back(0);
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) cout << ' ';
        cout << result[i];
    }
    cout << '\n';

    return 0;
}