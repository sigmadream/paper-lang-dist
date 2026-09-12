#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, k;
    if (!(cin >> n >> k)) return 0;
    
    vector<int> q;
    for (int i = 1; i <= n; i++) q.push_back(i);
    
    cout << "<";
    int idx = 0;
    while (!q.empty()) {
        idx = (idx + k - 1) % q.size();
        cout << q[idx];
        q.erase(q.begin() + idx);
        if (!q.empty()) cout << ", ";
    }
    cout << ">\n";
    return 0;
}
