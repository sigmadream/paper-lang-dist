#include <iostream>
#include <vector>
#include <cstdio>

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    
    std::vector<int> q(n);
    for (int i = 0; i < n; i++) q[i] = i + 1;
    
    std::cout << "<";
    int idx = 0;
    while (n > 0) {
        idx = (idx + k - 1) % n;
        std::cout << q[idx];
        n--;
        if (n > 0) std::cout << ", ";
        for (int i = idx; i < n; i++) q[i] = q[i + 1];
    }
    std::cout << ">\n";
    return 0;
}
