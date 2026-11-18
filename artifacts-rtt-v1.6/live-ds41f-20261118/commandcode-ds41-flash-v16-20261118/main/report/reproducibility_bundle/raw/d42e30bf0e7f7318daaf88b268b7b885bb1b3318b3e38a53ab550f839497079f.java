import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        long[] a = new long[n];

        int idx = 0;
        while (idx < n) {
            if (st.hasMoreTokens()) {
                a[idx++] = Long.parseLong(st.nextToken());
            } else {
                String line = br.readLine();
                if (line == null) break;
                st = new StringTokenizer(line);
            }
        }

        long cur = a[0];
        long best = a[0];

        for (int i = 1; i < n; i++) {
            cur = Math.max(a[i], cur + a[i]);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}