import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        if (!st.hasMoreTokens()) return;
        int m = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());

        long[] dp = new long[n];
        Arrays.fill(dp, 1);

        for (int i = 1; i < m; ++i) {
            for (int j = 1; j < n; ++j) {
                dp[j] += dp[j - 1];
            }
        }

        System.out.println(dp[n - 1]);
    }
}