#include <iostream>
#include <queue>

int main() {
    int n, k;
    std::cin >> n >> k;
    
    std::queue<int> queue;
    for (int i = 1; i <= n; i++) {
        queue.push(i);
    }
    
    std::cout << "<";
    int idx = 0;
    while (!queue.empty()) {
        idx = (idx + k - 1) % queue.size();
        std::cout << queue.front();
        queue.pop();
        if (!queue.empty()) {
            std::cout << ", ";
        }
    }
    std::cout << ">";
    
    return 0;
}
