import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] grid = new String[n];
        for (int i = 0; i < n; i++) {
            grid[i] = br.readLine().trim();
        }
        System.out.println(solve(grid, 0, 0, n));
    }

    private static String solve(String[] grid, int r, int c, int size) {
        char first = grid[r].charAt(c);
        boolean same = true;
        outer:
        for (int i = r; i < r + size; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i].charAt(j) != first) {
                    same = false;
                    break outer;
                }
            }
        }
        if (same) {
            return Character.toString(first);
        }

        int half = size / 2;
        String tl = solve(grid, r, c, half);
        String tr = solve(grid, r, c + half, half);
        String bl = solve(grid, r + half, c, half);
        String br = solve(grid, r + half, c + half, half);

        return "(" + tl + tr + bl + br + ")";
    }
}