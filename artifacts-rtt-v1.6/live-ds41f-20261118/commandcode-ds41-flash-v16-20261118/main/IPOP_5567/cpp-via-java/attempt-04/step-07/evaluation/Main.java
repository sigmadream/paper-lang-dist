import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);

        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) st.nval;

        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int m = (int) st.nval;

        List<Integer>[] adj = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) {
            adj[i] = new ArrayList<>();
        }

        for (int i = 0; i < m; i++) {
            st.nextToken();
            int u = (int) st.nval;
            st.nextToken();
            int v = (int) st.nval;

            adj[u].add(v);
            adj[v].add(u);
        }

        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);

        Queue<Integer> q = new ArrayDeque<>();
        dist[1] = 0;
        q.add(1);

        int ans = 0;

        while (!q.isEmpty()) {
            int cur = q.poll();

            for (int next : adj[cur]) {
                if (dist[next] == -1) {
                    dist[next] = dist[cur] + 1;
                    q.add(next);

                    if (dist[next] <= 2) {
                        ans++;
                    }
                }
            }
        }

        System.out.println(ans);
    }
}