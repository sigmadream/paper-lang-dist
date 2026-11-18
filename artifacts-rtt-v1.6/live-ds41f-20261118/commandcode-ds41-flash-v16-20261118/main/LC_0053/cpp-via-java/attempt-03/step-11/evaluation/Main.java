import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        if (!st.hasMoreTokens()) return;
        int n;
        try {
            n = Integer.parseInt(st.nextToken());
        } catch (Exception e) {
            return;
        }

        while (!st.hasMoreTokens()) {
            String line = br.readLine();
            if (line == null) return;
            st = new StringTokenizer(line);
        }

        long first;
        try {
            first = Long.parseLong(st.nextToken());
        } catch (Exception e) {
            return;
        }

        long cur = first;
        long best = first;

        for (int i = 1; i < n; i++) {
            while (!st.hasMoreTokens()) {
                String line = br.readLine();
                if (line == null) {
                    System.out.println(best);
                    return;
                }
                st = new StringTokenizer(line);
            }

            long x;
            try {
                x = Long.parseLong(st.nextToken());
            } catch (Exception e) {
                break;
            }

            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}