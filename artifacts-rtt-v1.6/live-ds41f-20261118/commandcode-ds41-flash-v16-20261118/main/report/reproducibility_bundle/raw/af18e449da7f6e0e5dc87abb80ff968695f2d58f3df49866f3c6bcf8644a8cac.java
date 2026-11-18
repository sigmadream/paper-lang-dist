import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int n;
    static int ans = 0;
    static int[] col = new int[15];
    static int[] diag1 = new int[29];
    static int[] diag2 = new int[29];

    static void solve(int r) {
        if (r == n) {
            ++ans;
            return;
        }
        for (int c = 0; c < n; ++c) {
            if (col[c] == 1 || diag1[r + c] == 1 || diag2[r - c + n - 1] == 1) continue;
            col[c] = 1;
            diag1[r + c] = 1;
            diag2[r - c + n - 1] = 1;

            solve(r + 1);

            col[c] = 0;
            diag1[r + c] = 0;
            diag2[r - c + n - 1] = 0;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        line = line.trim();
        if (line.isEmpty()) return;

        n = Integer.parseInt(line);

        solve(0);
        System.out.println(ans);
    }
}