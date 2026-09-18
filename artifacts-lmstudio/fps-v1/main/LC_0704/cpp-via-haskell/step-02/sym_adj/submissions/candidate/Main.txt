#include <iostream>
#include <vector>
using namespace std;

int binarySearch(int lo, int hi, int target, const vector<int>& a) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target)
            lo = mid + 1;
        else
            hi = mid;
    }
    return (lo == a.size() || a[lo] != target) ? -1 : lo;
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> a(n);
    for (int i = 0; i < n; ++i)
        cin >> a[i];
    
    int result = binarySearch(0, n, target, a);
    cout << result << endl;

    return 0;
}