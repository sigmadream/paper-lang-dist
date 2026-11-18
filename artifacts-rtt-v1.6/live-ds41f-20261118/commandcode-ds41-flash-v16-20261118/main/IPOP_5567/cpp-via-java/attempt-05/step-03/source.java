import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String line = br.readLine();
        if (line == null) return;

        int n = Integer.parseInt(line.trim());

        line = br.readLine();
        if (line == null) return;

        int m = Integer.parseInt(line.trim());

        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            adj.add(new ArrayList<>());
        }

        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());

            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);

        Queue<Integer> q = new LinkedList<>();
        q.offer(1);
        dist[1] = 0;

        int ans = 0;

        while (!q.isEmpty()) {
            int curr = q.poll();

            for (int nextNode : adj.get(curr)) {
                if (dist[nextNode] == -1) {
                    dist[nextNode] = dist[curr] + 1;
                    q.offer(nextNode);

                    if (dist[nextNode] <= 2) {
                        ans++;
                    }
                }
            }
        }

        System.out.println(ans);
    }
}