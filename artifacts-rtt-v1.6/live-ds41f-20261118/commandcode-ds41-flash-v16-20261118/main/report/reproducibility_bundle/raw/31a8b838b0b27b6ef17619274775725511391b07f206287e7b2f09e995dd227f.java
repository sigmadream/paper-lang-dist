import java.io.*;
import java.util.*;

public class Main {
    static class FastScanner {
        BufferedReader br;
        StringTokenizer st;

        FastScanner() {
            br = new BufferedReader(new InputStreamReader(System.in));
        }

        String next() {
            while (st == null || !st.hasMoreTokens()) {
                try {
                    String line = br.readLine();
                    if (line == null) return null;
                    st = new StringTokenizer(line);
                } catch (IOException e) {
                    return null;
                }
            }
            return st.nextToken();
        }

        int nextInt() {
            String s = next();
            return s == null ? -1 : Integer.parseInt(s);
        }
    }

    public static void main(String[] args) {
        FastScanner fs = new FastScanner();

        String ns = fs.next();
        if (ns == null) return;
        int n = Integer.parseInt(ns);

        String ms = fs.next();
        if (ms == null) return;
        int m = Integer.parseInt(ms);

        ArrayList<Integer>[] adj = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) {
            adj[i] = new ArrayList<>();
        }

        for (int i = 0; i < m; i++) {
            int u = fs.nextInt();
            int v = fs.nextInt();
            adj[u].add(v);
            adj[v].add(u);
        }

        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);

        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(1);
        dist[1] = 0;

        int ans = 0;

        while (!q.isEmpty()) {
            int curr = q.poll();

            for (int nextNode : adj[curr]) {
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