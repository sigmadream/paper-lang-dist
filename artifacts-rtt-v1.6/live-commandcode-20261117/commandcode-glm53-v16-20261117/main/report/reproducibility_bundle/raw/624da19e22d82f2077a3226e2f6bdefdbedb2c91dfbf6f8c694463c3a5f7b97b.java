import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumbers();
        st.nextToken();
        int m = (int) st.nval;
        st.nextToken();
        int n = (int) st.nval;
        long[] dp = new long[n];
        Arrays.fill(dp, 1L);
        for (int i = 1; i < m; ++i)
            for (int j = 1; j < n; ++j)
                dp[j] += dp[j - 1];
        System.out.println(dp[n - 1]);
    }
}