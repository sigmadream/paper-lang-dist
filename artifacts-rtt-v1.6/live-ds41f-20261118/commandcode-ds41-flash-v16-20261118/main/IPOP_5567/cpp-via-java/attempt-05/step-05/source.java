import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static class FastScanner {
        private final BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        private StringTokenizer st = new StringTokenizer("");

        String next() throws IOException {
            while (!st.hasMoreTokens()) {
                String line = br.readLine();
                if (line == null) return null;
                st = new StringTokenizer(line);
            }
            return st.nextToken();
        }

        int nextInt() throws IOException {
            String s = next();
            if (s == null) return -1;
            return Integer.parseInt(s);
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();

        String nToken = fs.next();
        if (nToken == null) return;
        int n = Integer.parseInt(nToken);

        String mToken = fs.next();
        if (mToken == null) return;
        int m = Integer.parseInt(mToken);

        if (n <= 0) {
            System.out.println(0);
            return;
        }

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

        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(1);
        dist[1] = 0;

        int answer = 0;

        while (!queue.isEmpty()) {
            int current = queue.poll();

            for (int next : adj[current]) {
                if (dist[next] == -1) {
                    dist[next] = dist[current] + 1;
                    queue.add(next);

                    if (dist[next] <= 2) {
                        answer++;
                    }
                }
            }
        }

        System.out.println(answer);
    }
}