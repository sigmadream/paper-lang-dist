import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 255);
        st.wordChars(33, 126);
        st.whitespaceChars(0, 32);
        st.parseNumbers();

        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) st.nval;
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int m = (int) st.nval;

        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
        for (int i = 0; i < m; i++) {
            st.nextToken();
            int u = (int) st.nval;
            st.nextToken();
            int v = (int) st.nval;
            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);
        Deque<Integer> q = new ArrayDeque<>();
        q.add(1);
        dist[1] = 0;
        int ans = 0;

        while (!q.isEmpty()) {
            int curr = q.poll();
            for (int next : adj.get(curr)) {
                if (dist[next] == -1) {
                    dist[next] = dist[curr] + 1;
                    q.add(next);
                    if (dist[next] <= 2) ans++;
                }
            }
        }

        System.out.println(ans);
    }
}