#include <iostream>
#include <vector>

int main() {
    int n;
    long long m;
    std::cin >> n >> m;
    
    std::vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        std::cin >> a[i];
    }
    
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
    
    std::cout << ans << std::endl;
    return 0;
}
