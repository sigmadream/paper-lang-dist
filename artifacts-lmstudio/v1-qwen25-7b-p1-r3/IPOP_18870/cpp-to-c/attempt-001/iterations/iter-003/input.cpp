#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;
    
    std::vector<int> a(n);
    for (int i = 0; i < n; i++) std::cin >> a[i];
    
    std::vector<int> sorted_a = a;
    std::sort(sorted_a.begin(), sorted_a.end());
    
    std::vector<int> unique_a;
    for (int i = 0; i < n; i++) {
        if (i == 0 || sorted_a[i] != sorted_a[i - 1]) {
            unique_a.push_back(sorted_a[i]);
        }
    }
    
    for (int i = 0; i < n; i++) {
        int compressed = 0;
        for (int j = 0; j < unique_a.size(); j++) {
            if (a[i] > unique_a[j]) compressed++;
        }
        std::cout << compressed << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
