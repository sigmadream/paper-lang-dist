import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        Integer nObj = fs.nextIntNullable();
        if (nObj == null) return;
        int n = nObj;
        int m = fs.nextInt();

        ArrayList<Integer>[] adj = new ArrayList[n + 1];
        for (int i = 0; i <= n; i++) adj[i] = new ArrayList<>();

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

        System.out.print(ans + "\n");
    }

    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream is) {
            in = is;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        Integer nextIntNullable() throws IOException {
            int c;
            do {
                c = read();
                if (c == -1) return null;
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + (c - '0');
                c = read();
            }
            return val * sign;
        }

        int nextInt() throws IOException {
            return nextIntNullable();
        }
    }
}
