import java.util.Scanner;

public class Main {
    private static int n;
    private static int ans = 0;
    private static int[] col = new int[15];
    private static int[] diag1 = new int[29];
    private static int[] diag2 = new int[29];

    private static void solve(int r) {
        if (r == n) {
            ++ans;
            return;
        }

        for (int c = 0; c < n; ++c) {
            if (col[c] == 1 || diag1[r + c] == 1 || diag2[r - c + n - 1] == 1) {
                continue;
            }

            col[c] = 1;
            diag1[r + c] = 1;
            diag2[r - c + n - 1] = 1;

            solve(r + 1);

            col[c] = 0;
            diag1[r + c] = 0;
            diag2[r - c + n - 1] = 0;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        if (!scanner.hasNextInt()) {
            return;
        }

        n = scanner.nextInt();
        solve(0);
        System.out.println(ans);
    }
}