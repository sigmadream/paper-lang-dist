import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line);

        long[] a = new long[n];
        int idx = 0;
        while (idx < n) {
            String l = br.readLine();
            if (l == null) break;
            st = new StringTokenizer(l);
            while (st.hasMoreTokens() && idx < n) {
                a[idx++] = Long.parseLong(st.nextToken());
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

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; ++i) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        sb.append('\n');
        System.out.print(sb.toString());
    }
}