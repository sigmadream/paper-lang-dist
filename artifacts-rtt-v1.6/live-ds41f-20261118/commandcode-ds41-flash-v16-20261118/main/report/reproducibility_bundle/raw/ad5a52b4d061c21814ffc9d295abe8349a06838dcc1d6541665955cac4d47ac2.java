import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int[] counts = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            counts[i] = counts[i / 2] + (i % 2);
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(counts[i]);
        }
        sb.append('\n');
        System.out.print(sb);
    }
}