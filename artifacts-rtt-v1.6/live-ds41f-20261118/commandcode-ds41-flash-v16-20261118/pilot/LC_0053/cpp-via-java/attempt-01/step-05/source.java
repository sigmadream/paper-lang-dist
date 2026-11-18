import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        if (!st.hasMoreTokens()) return;

        int n = Integer.parseInt(st.nextToken());

        StringBuilder sb = new StringBuilder();
        while (st.hasMoreTokens()) {
            sb.append(st.nextToken()).append(' ');
        }

        if (n > 0 && sb.length() == 0) {
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line).append(' ');
            }
        } else {
            String line;
            int count = 0;
            for (int i = 0; i < sb.length(); i++) {
                if (sb.charAt(i) == ' ') count++;
            }
            while (count < n && (line = br.readLine()) != null) {
                sb.append(line).append(' ');
                for (int i = 0; i < line.length(); i++) {
                    if (line.charAt(i) == ' ') count++;
                }
                if (line.trim().length() > 0) count++;
            }
        }

        st = new StringTokenizer(sb.toString());
        long x = Long.parseLong(st.nextToken());
        long cur = x;
        long best = x;

        for (int i = 1; i < n; ++i) {
            x = Long.parseLong(st.nextToken());
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}