import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        int n;
        try {
            String line = br.readLine();
            if (line == null) return;
            line = line.trim();
            if (line.isEmpty()) return;
            n = Integer.parseInt(line);
        } catch (Exception e) {
            return;
        }

        long[] a = new long[n];
        long[] tmp = new long[n];
        int cnt = 0;
        StringBuilder data = new StringBuilder();
        String l;
        while (cnt < n && (l = br.readLine()) != null) {
            data.append(l).append(' ');
        }
        String[] tokens = data.toString().trim().split("\\s+");
        int m = Math.min(n, tokens.length);
        for (int i = 0; i < m; ++i) {
            if (tokens[i].isEmpty()) continue;
            a[i] = Long.parseLong(tokens[i]);
        }

        int write = 0;
        for (int read = 0; read < n; ++read) {
            if (a[read] != 0) {
                long t = a[write];
                a[write] = a[read];
                a[read] = t;
                ++write;
            }
        }

        for (int i = 0; i < n; ++i) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        sb.append('\n');
        System.out.print(sb.toString());
    }
}