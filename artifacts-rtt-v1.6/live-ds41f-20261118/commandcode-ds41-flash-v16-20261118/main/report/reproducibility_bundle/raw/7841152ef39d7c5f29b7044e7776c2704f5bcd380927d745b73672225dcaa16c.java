import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        int n = 0;
        try {
            String[] parts = line.trim().split("\\s+");
            if (parts.length == 0 || parts[0].isEmpty()) return;
            n = Integer.parseInt(parts[0]);
        } catch (Exception e) {
            return;
        }

        long[] a = new long[n];
        int idx = 0;
        while (idx < n) {
            String l = br.readLine();
            if (l == null) break;
            StringTokenizer st = new StringTokenizer(l);
            while (idx < n && st.hasMoreTokens()) {
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

        StringBuilder out = new StringBuilder();
        for (int i = 0; i < n; ++i) {
            if (i > 0) out.append(' ');
            out.append(a[i]);
        }
        out.append('\n');
        System.out.print(out);
    }
}