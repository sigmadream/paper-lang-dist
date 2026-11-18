import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        int[] score = new int[n + 1];
        int[] dp = new int[n + 1];
        for (int index = 1; index <= n; ++index) {
            score[index] = Integer.parseInt(br.readLine().trim());
        }

        if (n >= 1) {
            dp[1] = score[1];
        }
        if (n >= 2) {
            dp[2] = score[1] + score[2];
        }
        for (int index = 3; index <= n; ++index) {
            dp[index] = Math.max(dp[index - 2], dp[index - 3] + score[index - 1]) + score[index];
        }

        System.out.println(dp[n]);
    }
}