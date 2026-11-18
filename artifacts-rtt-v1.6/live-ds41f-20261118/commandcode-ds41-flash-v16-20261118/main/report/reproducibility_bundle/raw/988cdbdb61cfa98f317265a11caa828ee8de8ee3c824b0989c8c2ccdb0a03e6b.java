import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        long[] a = new long[n];

        int idx = 0;
        while (idx < n) {
            if (!st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
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

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; ++i) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        sb.append('\n');

        System.out.print(sb);
    }
}