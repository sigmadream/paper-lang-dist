#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    long long m;
    if (!(cin >> n >> m)) return 0;
    
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    int ans = 0;
    long long sum = 0;
    int end = 0;
    
    for (int start = 0; start < n; start++) {
        while (sum < m && end < n) {
            sum += a[end];
            end++;
        }
        if (sum == m) ans++;
        sum -= a[start];
    }
    
    cout << ans << "\n";
    return 0;
}
