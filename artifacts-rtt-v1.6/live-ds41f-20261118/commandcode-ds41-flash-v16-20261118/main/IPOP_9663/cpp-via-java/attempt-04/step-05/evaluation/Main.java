import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int ans = 0;
    static int n;
    static boolean[] col, diag1, diag2;

    static void solve(int r) {
        if (r == n) {
            ans++;
            return;
        }
        for (int c = 0; c < n; c++) {
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
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;
        n = Integer.parseInt(line);

        col = new boolean[n];
        diag1 = new boolean[2 * n - 1];
        diag2 = new boolean[2 * n - 1];

        solve(0);

        System.out.println(ans);
    }
}