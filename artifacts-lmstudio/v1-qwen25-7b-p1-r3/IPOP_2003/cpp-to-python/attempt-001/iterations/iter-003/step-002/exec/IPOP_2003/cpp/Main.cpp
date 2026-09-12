#include <iostream>
#include <vector>

int count_subarrays_with_sum(int n, int m, const std::vector<int>& a) {
    int ans = 0;
    int sum = 0;
    int end = 0;
    
    for (int start = 0; start < n; ++start) {
        while (sum < m && end < n) {
            sum += a[end];
            ++end;
        }
        if (sum == m) {
            ++ans;
        }
        sum -= a[start];
    }
    
    return ans;
}

int main() {
    int n, m;
    std::cin >> n >> m;
    std::vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i];
    }

    std::cout << count_subarrays_with_sum(n, m, a) << std::endl;

    return 0;
}
