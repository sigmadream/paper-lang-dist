#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int h, w;
    if (!(cin >> h >> w)) return 0;
    
    vector<int> a(w);
    for (int i = 0; i < w; i++) cin >> a[i];
    
    int ans = 0;
    for (int i = 1; i < w - 1; i++) {
        int left_max = 0, right_max = 0;
        for (int j = 0; j <= i; j++) left_max = max(left_max, a[j]);
        for (int j = i; j < w; j++) right_max = max(right_max, a[j]);
        int bound = min(left_max, right_max);
        if (bound > a[i]) ans += bound - a[i];
    }
    
    cout << ans << "\n";
    return 0;
}
