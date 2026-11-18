import java.util.*;

public class Main {
    static int n;
    static long ans = 0;
    static char[] col, diag1, diag2;

    static void solve(int r) {
        if (r == n) { ans++; return; }
        for (int c = 0; c < n; c++) {
            if (col[c] != 0 || diag1[r + c] != 0 || diag2[r - c + n - 1] != 0) continue;
            col[c] = diag1[r + c] = diag2[r - c + n - 1] = 1;
            solve(r + 1);
            col[c] = diag1[r + c] = diag2[r - c + n - 1] = 0;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String line = sc.nextLine().trim();
        if (line.isEmpty()) return;
        n = Integer.parseInt(line);
        col = new char[n];
        diag1 = new char[2 * n - 1];
        diag2 = new char[2 * n - 1];
        solve(0);
        System.out.println(ans);
    }
}