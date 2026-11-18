import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String line = br.readLine();
        if (line == null) return;
        st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;
        int n = Integer.parseInt(st.nextToken());

        line = br.readLine();
        if (line == null) return;
        st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;
        int m = Integer.parseInt(st.nextToken());

        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            adj.add(new ArrayList<>());
        }

        for (int i = 0; i < m; i++) {
            line = br.readLine();
            if (line == null) break;
            st = new StringTokenizer(line);
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);

        Queue<Integer> q = new ArrayDeque<>();
        q.add(1);
        dist[1] = 0;

        int ans = 0;

        while (!q.isEmpty()) {
            int curr = q.poll();

            for (int nextNode : adj.get(curr)) {
                if (dist[nextNode] == -1) {
                    dist[nextNode] = dist[curr] + 1;
                    q.add(nextNode);

                    if (dist[nextNode] <= 2) {
                        ans++;
                    }
                }
            }
        }

        System.out.println(ans);
    }
}