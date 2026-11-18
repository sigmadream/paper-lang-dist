import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static int n;
    private static int ans = 0;
    private static boolean[] col;
    private static boolean[] diag1;
    private static boolean[] diag2;

    private static void solve(int r) {
        if (r == n) {
            ans++;
            return;
        }
        for (int c = 0; c < n; c++) {
            int d1 = r + c;
            int d2 = r - c + n - 1;
            if (col[c] || diag1[d1] || diag2[d2]) {
                continue;
            }
            col[c] = diag1[d1] = diag2[d2] = true;
            solve(r + 1);
            col[c] = diag1[d1] = diag2[d2] = false;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) {
            return;
        }

        n = Integer.parseInt(line.trim());

        col = new boolean[n];
        diag1 = new boolean[2 * n - 1];
        diag2 = new boolean[2 * n - 1];

        solve(0);
        System.out.println(ans);
    }
}