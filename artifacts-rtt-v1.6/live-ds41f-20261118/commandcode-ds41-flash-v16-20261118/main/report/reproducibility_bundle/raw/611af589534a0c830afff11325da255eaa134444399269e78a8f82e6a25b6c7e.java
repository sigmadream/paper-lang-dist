import java.io.*;
import java.util.*;

public class Main {
    static char[][] grid;

    static String solve(int r, int c, int size) {
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
        if (same) return String.valueOf(first);

        int half = size / 2;
        StringBuilder sb = new StringBuilder();
        sb.append('(');
        sb.append(solve(r, c, half));
        sb.append(solve(r, c + half, half));
        sb.append(solve(r + half, c, half));
        sb.append(solve(r + half, c + half, half));
        sb.append(')');
        return sb.toString();
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) return;

        int n = Integer.parseInt(line.trim());
        grid = new char[n][];
        for (int i = 0; i < n; i++) {
            String row = br.readLine();
            grid[i] = row.toCharArray();
        }

        StringBuilder out = new StringBuilder();
        out.append(solve(0, 0, n)).append('\n');
        System.out.print(out);
    }
}