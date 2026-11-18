#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }

    int pos = 0;
    for (int i = 0; i < n; ++i) {
        if (nums[i] != 0) {
            nums[pos++] = nums[i];
        }
    }
    while (pos < n) {
        nums[pos++] = 0;
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) cout << ' ';
        cout << nums[i];
    }
    cout << '\n';

    return 0;
}