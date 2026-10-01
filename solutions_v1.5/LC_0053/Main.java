import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = reader.readLine();
        if (line == null) return;
        StringTokenizer tokenizer = new StringTokenizer(line);
        while (!tokenizer.hasMoreTokens()) {
            line = reader.readLine();
            if (line == null) return;
            tokenizer = new StringTokenizer(line);
        }
        int n = Integer.parseInt(tokenizer.nextToken());
        while (!tokenizer.hasMoreTokens()) {
            line = reader.readLine();
            if (line == null) return;
            tokenizer = new StringTokenizer(line);
        }
        long first = Long.parseLong(tokenizer.nextToken());
        long cur = first;
        long best = first;
        for (int i = 1; i < n; i++) {
            while (!tokenizer.hasMoreTokens()) {
                line = reader.readLine();
                if (line == null) break;
                tokenizer = new StringTokenizer(line);
            }
            long val = Long.parseLong(tokenizer.nextToken());
            cur = Math.max(val, cur + val);
            best = Math.max(best, cur);
        }
        System.out.println(best);
    }
}
