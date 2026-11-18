import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            sb.append(line).append(' ');
        }
        StringTokenizer st = new StringTokenizer(sb.toString());
        if (!st.hasMoreTokens()) return;
        long n = Long.parseLong(st.nextToken());
        if (n <= 0) return;
        if (!st.hasMoreTokens()) return;
        long x = Long.parseLong(st.nextToken());

        long cur = x;
        long best = x;

        for (long i = 1; i < n; ++i) {
            if (!st.hasMoreTokens()) break;
            x = Long.parseLong(st.nextToken());
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}