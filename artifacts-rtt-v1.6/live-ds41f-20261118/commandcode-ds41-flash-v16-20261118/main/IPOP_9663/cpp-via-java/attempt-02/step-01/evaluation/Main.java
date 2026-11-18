import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int n;
    static int ans = 0;
    static boolean[] col;
    static boolean[] diag1;
    static boolean[] diag2;

    static void solve(int r) {
        if (r == n) {
            ans++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
            col[c] = true;
            diag1[r + c] = true;
            diag2[r - c + n - 1] = true;

            solve(r + 1);

            col[c] = false;
            diag1[r + c] = false;
            diag2[r - c + n - 1] = false;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        n = Integer.parseInt(line.trim());

        col = new boolean[n];
        diag1 = new boolean[2 * n - 1];
        diag2 = new boolean[2 * n - 1];

        solve(0);

        System.out.println(ans);
    }
}