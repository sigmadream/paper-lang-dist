#include <iostream>
#include <vector>
#include <queue>
#include <set>

int main() {
    int n, m;
    std::cin >> n >> m;
    std::vector<std::vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        std::cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    std::set<int> direct, two;
    std::queue<int> q;

    // Find all nodes directly connected to node 1
    for (int neighbor : adj[1]) {
        direct.insert(neighbor);
        q.push(neighbor);
    }

    // Find all nodes that are at distance 2 from node 1
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        for (int neighbor : adj[current]) {
            if (direct.find(neighbor) == direct.end() && two.find(neighbor) == two.end()) {
                two.insert(neighbor);
                q.push(neighbor);
            }
        }
    }

    // Output the number of nodes at distance 1 or 2 from node 1, excluding node 1 itself
    std::cout << (direct.size() + two.size()) << std::endl;

    return 0;
}