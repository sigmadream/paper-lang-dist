import java.io.*;
import java.util.*;

public class Main {
    static int n;
    static long ans;
    static boolean[] col = new boolean[15];
    static boolean[] diag1 = new boolean[30];
    static boolean[] diag2 = new boolean[30];

    static void solve(int r) {
        if (r == n) {
            ++ans;
            return;
        }
        for (int c = 0; c < n; ++c) {
            int d1 = r + c;
            int d2 = r - c + n - 1;
            if (col[c] || diag1[d1] || diag2[d2]) continue;
            col[c] = true;
            diag1[d1] = true;
            diag2[d2] = true;
            solve(r + 1);
            col[c] = false;
            diag1[d1] = false;
            diag2[d2] = false;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null || s.trim().isEmpty()) return;
        n = Integer.parseInt(s.trim());

        ans = 0;
        solve(0);

        System.out.println(ans);
    }
}