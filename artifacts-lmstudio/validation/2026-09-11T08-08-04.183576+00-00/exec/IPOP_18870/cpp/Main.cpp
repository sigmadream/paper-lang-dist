#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    vector<int> sorted_a = a;
    sort(sorted_a.begin(), sorted_a.end());
    sorted_a.erase(unique(sorted_a.begin(), sorted_a.end()), sorted_a.end());
    
    for (int i = 0; i < n; i++) {
        int compressed = lower_bound(sorted_a.begin(), sorted_a.end(), a[i]) - sorted_a.begin();
        cout << compressed << " ";
    }
    cout << "\n";
    return 0;
}
