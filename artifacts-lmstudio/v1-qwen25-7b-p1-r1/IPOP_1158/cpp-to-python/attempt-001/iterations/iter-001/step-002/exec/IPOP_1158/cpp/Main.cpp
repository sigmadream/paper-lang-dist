#include <iostream>
#include <vector>
#include <queue>

std::vector<int> josephus(int n, int k) {
    std::queue<int> q;
    for (int i = 1; i <= n; ++i) {
        q.push(i);
    }
    std::vector<int> result;
    int idx = 0;
    
    while (!q.empty()) {
        idx = (idx + k - 1) % q.size();
        for (int i = 0; i < idx; ++i) {
            q.push(q.front());
            q.pop();
        }
        result.push_back(q.front());
        q.pop();
    }
    
    return result;
}

int main() {
    int n, k;
    std::cin >> n >> k;
    std::vector<int> result = josephus(n, k);
    std::cout << "<";
    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << result[i];
    }
    std::cout << ">" << std::endl;
    
    return 0;
}
