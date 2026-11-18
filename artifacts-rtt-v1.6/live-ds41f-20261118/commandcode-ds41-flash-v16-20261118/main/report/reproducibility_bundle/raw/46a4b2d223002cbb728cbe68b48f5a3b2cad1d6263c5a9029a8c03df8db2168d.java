import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    static int n;
    static int ans = 0;
    static boolean[] col;
    static boolean[] diag1;
    static boolean[] diag2;

    static void solve(int r) {
        if (r == n) {
            ++ans;
            return;
        }

        for (int c = 0; c < n; ++c) {
            int d1 = r + c;
            int d2 = r - c + n - 1;

            if (col[c] || diag1[d1] || diag2[d2]) continue;

            col[c] = diag1[d1] = diag2[d2] = true;
            solve(r + 1);
            col[c] = diag1[d1] = diag2[d2] = false;
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;
        n = Integer.parseInt(line);

        col = new boolean[n];
        diag1 = new boolean[2 * n];
        diag2 = new boolean[2 * n];

        solve(0);
        System.out.println(ans);
    }
}