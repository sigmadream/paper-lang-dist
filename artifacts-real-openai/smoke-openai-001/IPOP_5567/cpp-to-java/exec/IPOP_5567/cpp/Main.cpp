    while (!q.empty()) {
        int curr = q.front();
        q.pop();
        for (int nextNode : adj[curr]) {
            if (dist[nextNode] == -1) {
                dist[nextNode] = dist[curr] + 1;
                q.push(nextNode);
                if (dist[nextNode] <= 2) {
                    ans++;
                }
            }
        }
    }
