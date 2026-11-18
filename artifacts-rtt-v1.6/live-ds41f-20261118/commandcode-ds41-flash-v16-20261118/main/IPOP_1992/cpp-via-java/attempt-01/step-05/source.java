import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    private static char[][] grid;

    private static String solve(int r, int c, int size) {
        char first = grid[r][c];
        boolean same = true;

        for (int i = r; i < r + size && same; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i][j] != first) {
                    same = false;
                    break;
                }
            }
        }

        if (same) {
            return String.valueOf(first);
        }

        int half = size / 2;
        StringBuilder result = new StringBuilder();
        result.append('(');
        result.append(solve(r, c, half));
        result.append(solve(r, c + half, half));
        result.append(solve(r + half, c, half));
        result.append(solve(r + half, c + half, half));
        result.append(')');
        return result.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String line = br.readLine();
        if (line == null) return;

        String trimmed = line.trim();
        if (trimmed.isEmpty()) return;

        int n = Integer.parseInt(trimmed);
        grid = new char[n][];

        for (int i = 0; i < n; i++) {
            String row = br.readLine();
            if (row == null) row = "";
            grid[i] = row.toCharArray();
        }

        StringBuilder out = new StringBuilder();
        out.append(solve(0, 0, n));
        out.append('\n');
        System.out.print(out);
    }
}