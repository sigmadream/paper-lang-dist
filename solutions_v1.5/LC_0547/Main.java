import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = reader.readLine();
        if (line == null) return;
        StringTokenizer tokenizer = new StringTokenizer(line);
        while (!tokenizer.hasMoreTokens()) {
            line = reader.readLine();
            if (line == null) return;
            tokenizer = new StringTokenizer(line);
        }
        int n = Integer.parseInt(tokenizer.nextToken());
        int[][] g = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                while (!tokenizer.hasMoreTokens()) {
                    line = reader.readLine();
                    if (line == null) break;
                    tokenizer = new StringTokenizer(line);
                }
                g[i][j] = Integer.parseInt(tokenizer.nextToken());
            }
        }
        boolean[] seen = new boolean[n];
        int components = 0;
        for (int i = 0; i < n; i++) {
            if (!seen[i]) {
                components++;
                Deque<Integer> stack = new ArrayDeque<>();
                stack.push(i);
                seen[i] = true;
                while (!stack.isEmpty()) {
                    int u = stack.pop();
                    for (int v = 0; v < n; v++) {
                        if (g[u][v] == 1 && !seen[v]) {
                            seen[v] = true;
                            stack.push(v);
                        }
                    }
                }
            }
        }
        System.out.println(components);
    }
}
