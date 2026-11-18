import java.util.Scanner;

public class Main {
    static int n;
    static int ans = 0;
    static boolean[] col = new boolean[15];
    static boolean[] diag1 = new boolean[29];
    static boolean[] diag2 = new boolean[29];

    static void solve(int r) {
        if (r == n) {
            ++ans;
            return;
        }

        for (int c = 0; c < n; ++c) {
            int d1 = r + c;
            int d2 = r - c + n - 1;

            if (col[c] || diag1[d1] || diag2[d2]) {
                continue;
            }

            col[c] = true;
            diag1[d1] = true;
            diag2[d2] = true;

            solve(r + 1);

            col[c] = false;
            diag1[d1] = false;
            diag2[d2] = false;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            return;
        }
        n = sc.nextInt();

        for (int i = 0; i < n; ++i) {
            col[i] = false;
        }
        for (int i = 0; i < 2 * n - 1; ++i) {
            diag1[i] = false;
            diag2[i] = false;
        }

        solve(0);
        System.out.println(ans);
    }
}