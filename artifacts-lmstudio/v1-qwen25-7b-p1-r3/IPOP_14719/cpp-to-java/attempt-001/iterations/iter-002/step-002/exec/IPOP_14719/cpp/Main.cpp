#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int h, w;
    std::cin >> h >> w;
    
    std::vector<int> a(w);
    for (int i = 0; i < w; i++) {
        std::cin >> a[i];
    }
    
    int ans = 0;
    for (int i = 1; i < w - 1; i++) {
        int left_max = 0, right_max = 0;
        for (int j = 0; j <= i; j++) {
            left_max = std::max(left_max, a[j]);
        }
        for (int j = i; j < w; j++) {
            right_max = std::max(right_max, a[j]);
        }
        int bound = std::min(left_max, right_max);
        if (bound > a[i]) {
            ans += bound - a[i];
        }
    }
    
    std::cout << ans << std::endl;
    return 0;
}
