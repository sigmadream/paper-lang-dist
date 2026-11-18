import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long m = sc.nextLong(), n = sc.nextLong();
        long[] dp = new long[(int) n];
        Arrays.fill(dp, 1L);
        for (long i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                dp[j] += dp[j - 1];
        System.out.println(dp[(int) (n - 1)]);
    }
}