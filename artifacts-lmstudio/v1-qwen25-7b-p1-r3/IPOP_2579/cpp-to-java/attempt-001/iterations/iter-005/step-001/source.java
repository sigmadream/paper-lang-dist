import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();

        int[] score = new int[n + 1];
        int[] dp = new int[n + 1];
        for (int index = 1; index <= n; ++index) {
            score[index] = scanner.nextInt();
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
