import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String line = br.readLine();
        if (line == null) return;

        line = line.trim();
        if (line.isEmpty()) return;

        int n;
        try {
            n = (int) Long.parseLong(line);
        } catch (NumberFormatException e) {
            return;
        }

        long[] a = new long[n];
        int idx = 0;

        while (idx < n) {
            String l = br.readLine();
            if (l == null) break;

            StringTokenizer st = new StringTokenizer(l);
            while (idx < n && st.hasMoreTokens()) {
                String tok = st.nextToken();
                try {
                    long val = Long.parseLong(tok);
                    a[idx++] = val;
                } catch (NumberFormatException e) {
                    break;
                }
            }
        }

        int write = 0;
        for (int read = 0; read < n; ++read) {
            if (a[read] != 0) {
                long tmp = a[write];
                a[write] = a[read];
                a[read] = tmp;
                ++write;
            }
        }

        StringBuilder out = new StringBuilder();
        for (int i = 0; i < n; ++i) {
            if (i > 0) out.append(' ');
            out.append(a[i]);
        }
        out.append('\n');

        System.out.print(out.toString());
    }
}