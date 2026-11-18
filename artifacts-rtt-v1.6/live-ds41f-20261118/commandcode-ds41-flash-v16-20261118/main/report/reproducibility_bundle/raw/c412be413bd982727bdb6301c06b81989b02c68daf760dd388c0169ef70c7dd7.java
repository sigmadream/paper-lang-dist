import java.util.Scanner;

public class Main {
    static int N;
    static String[] grid;

    static String solve(int r, int c, int size) {
        char first = grid[r].charAt(c);
        boolean same = true;

        for (int i = r; i < r + size && same; ++i) {
            for (int j = c; j < c + size; ++j) {
                if (grid[i].charAt(j) != first) {
                    same = false;
                    break;
                }
            }
        }

        if (same) return String.valueOf(first);

        int half = size / 2;
        String tl = solve(r, c, half);
        String tr = solve(r, c + half, half);
        String bl = solve(r + half, c, half);
        String br = solve(r + half, c + half, half);

        return "(" + tl + tr + bl + br + ")";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;

        N = sc.nextInt();
        grid = new String[N];
        for (int i = 0; i < N; ++i) {
            grid[i] = sc.next();
        }

        System.out.println(solve(0, 0, N));
    }
}