#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;

    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }

    int index = 0;
    for (int i = 0; i < n; ++i) {
        if (nums[i] != 0) {
            nums[index++] = nums[i];
        }
    }
    while (index < n) {
        nums[index++] = 0;
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) cout << ' ';
        cout << nums[i];
    }
    cout << '\n';

    return 0;
}