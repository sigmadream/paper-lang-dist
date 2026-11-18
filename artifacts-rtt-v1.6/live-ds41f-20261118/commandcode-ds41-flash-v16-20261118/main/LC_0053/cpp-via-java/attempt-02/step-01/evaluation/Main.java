import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long cur = 0, best = Long.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            long x = Long.parseLong(st.nextToken());
            if (i == 0) {
                cur = x;
                best = x;
            } else {
                cur = Math.max(x, cur + x);
                best = Math.max(best, cur);
            }
        }
        System.out.println(best);
    }
}