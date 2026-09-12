import java.util.Scanner;

public class QuadTreeCompression {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        scanner.nextLine();
        String[] grid = new String[n];
        for (int i = 0; i < n; i++) {
            grid[i] = scanner.nextLine();
        }
        System.out.println(solve(grid, 0, 0, n));
    }

    public static String solve(String[] grid, int r, int c, int size) {
        char first = grid[r].charAt(c);
        boolean same = true;
        for (int i = r; i < r + size; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i].charAt(j) != first) {
                    same = false;
                    break;
                }
            }
            if (!same) break;
        }

        if (same) return String.valueOf(first);

        int half = size / 2;
        String tl = solve(grid, r, c, half);
        String tr = solve(grid, r, c + half, half);
        String bl = solve(grid, r + half, c, half);
        String br = solve(grid, r + half, c + half, half);

        return "(" + tl + tr + bl + br + ")";
    }
}
