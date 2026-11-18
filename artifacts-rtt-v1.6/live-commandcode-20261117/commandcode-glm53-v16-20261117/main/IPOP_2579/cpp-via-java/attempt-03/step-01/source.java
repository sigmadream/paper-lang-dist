import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int[] score = new int[n + 1];
        int[] d = new int[n + 1];
        for (int i = 1; i <= n; ++i) {
            score[i] = Integer.parseInt(br.readLine().trim());
        }
        if (n >= 1) d[1] = score[1];
        if (n >= 2) d[2] = score[1] + score[2];
        for (int i = 3; i <= n; ++i) {
            d[i] = Math.max(d[i - 2], d[i - 3] + score[i - 1]) + score[i];
        }
        System.out.println(d[n]);
    }
}