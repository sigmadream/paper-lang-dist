import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = reader.readLine();
        if (line == null) return;
        StringTokenizer tokenizer = new StringTokenizer(line);
        if (!tokenizer.hasMoreTokens()) return;
        int n = Integer.parseInt(tokenizer.nextToken());
        int[] dp = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            dp[i] = dp[i >> 1] + (i & 1);
        }
        PrintWriter writer = new PrintWriter(System.out);
        for (int i = 0; i <= n; i++) {
            if (i > 0) writer.print(' ');
            writer.print(dp[i]);
        }
        writer.println();
        writer.flush();
    }
}
