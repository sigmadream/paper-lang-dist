import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
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

        long nextLong() throws IOException {
            return Long.parseLong(next());
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();

        String first = fs.next();
        if (first == null) return;

        int n = Integer.parseInt(first);
        if (n <= 0) return;

        long x = fs.nextLong();
        long cur = x;
        long best = x;

        for (int i = 1; i < n; ++i) {
            x = fs.nextLong();
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}