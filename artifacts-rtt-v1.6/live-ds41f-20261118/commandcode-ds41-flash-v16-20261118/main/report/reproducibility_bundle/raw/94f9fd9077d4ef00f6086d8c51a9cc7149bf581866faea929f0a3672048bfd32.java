import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String firstLine = br.readLine();
        if (firstLine == null) return;

        int n = Integer.parseInt(firstLine.trim());

        StringTokenizer st = new StringTokenizer(br.readLine());
        long first = Long.parseLong(st.nextToken());

        long cur = first;
        long best = first;

        for (int i = 1; i < n; ++i) {
            long x = Long.parseLong(st.nextToken());
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}