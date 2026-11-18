import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;
        int n = Integer.parseInt(line);

        long first = 0;
        boolean hasFirst = false;
        while (!hasFirst) {
            String l = br.readLine();
            if (l == null) return;
            st = new StringTokenizer(l);
            if (st.hasMoreTokens()) {
                first = Long.parseLong(st.nextToken());
                hasFirst = true;
                break;
            }
        }

        long cur = first;
        long best = first;
        int count = 1;

        while (count < n) {
            String l = br.readLine();
            if (l == null) break;
            st = new StringTokenizer(l);
            while (st.hasMoreTokens() && count < n) {
                long x = Long.parseLong(st.nextToken());
                cur = Math.max(x, cur + x);
                best = Math.max(best, cur);
                count++;
            }
        }

        System.out.println(best);
    }
}