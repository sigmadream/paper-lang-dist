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
        int leftMax = 0, rightMax = 0;
        for (int j = 0; j <= i; j++) {
            leftMax = std::max(leftMax, a[j]);
        }
        for (int j = i; j < w; j++) {
            rightMax = std::max(rightMax, a[j]);
        }
        int bound = std::min(leftMax, rightMax);
        if (bound > a[i]) {
            ans += bound - a[i];
        }
    }
    
    std::cout << ans << std::endl;
    return 0;
}
