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

        int n = Integer.parseInt(st.nextToken());
        long cur = Long.parseLong(st.nextToken());
        long best = cur;

        for (int i = 1; i < n; ++i) {
            long x = Long.parseLong(st.nextToken());
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}