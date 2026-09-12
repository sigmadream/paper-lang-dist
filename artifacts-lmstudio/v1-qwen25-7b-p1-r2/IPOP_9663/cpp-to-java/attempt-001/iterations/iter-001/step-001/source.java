import java.util.Scanner;

public class NQueen {
    static int ans = 0;
    static int n;
    static boolean[] col, diag1, diag2;

    static void solve(int r) {
        if (r == n) {
            ans++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
            col[c] = diag1[r + c] = diag2[r - c + n - 1] = true;
            solve(r + 1);
            col[c] = diag1[r + c] = diag2[r - c + n - 1] = false;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        n = scanner.nextInt();
        
        col = new boolean[n];
        diag1 = new boolean[2 * n - 1];
        diag2 = new boolean[2 * n - 1];
        solve(0);
        
        System.out.println(ans);
    }
}
