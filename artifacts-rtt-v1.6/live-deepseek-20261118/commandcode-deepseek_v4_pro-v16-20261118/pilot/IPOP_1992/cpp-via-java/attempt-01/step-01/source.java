import java.io.*;

public class Main {
    static String solve(char[][] grid, int r, int c, int size) {
        char first = grid[r][c];
        boolean same = true;
        outer:
        for (int i = r; i < r + size; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i][j] != first) {
                    same = false;
                    break outer;
                }
            }
        }
        if (same) return String.valueOf(first);
        int half = size / 2;
        String tl = solve(grid, r, c, half);
        String tr = solve(grid, r, c + half, half);
        String bl = solve(grid, r + half, c, half);
        String br = solve(grid, r + half, c + half, half);
        return "(" + tl + tr + bl + br + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int n = Integer.parseInt(line.trim());
        char[][] grid = new char[n][n];
        for (int i = 0; i < n; i++) {
            String row = br.readLine();
            grid[i] = row.toCharArray();
        }
        System.out.println(solve(grid, 0, 0, n));
    }
}