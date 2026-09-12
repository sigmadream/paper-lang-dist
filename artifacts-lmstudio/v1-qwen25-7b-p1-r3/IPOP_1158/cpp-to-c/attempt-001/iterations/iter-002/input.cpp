#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, k;
    if (cin >> n >> k) {
        vector<int> q(n);
        for (int i = 0; i < n; i++) q[i] = i + 1;
        
        cout << "<";
        int idx = 0;
        while (n > 0) {
            idx = (idx + k - 1) % n;
            cout << q[idx];
            n--;
            if (n > 0) cout << ", ";
            for (int i = idx; i < n; i++) q[i] = q[i + 1];
        }
        cout << ">\n";
    }
    return 0;
}
