import java.io.*;
import java.util.*;

public class Main {
    static int n;
    static char[][] grid;
    static StringBuilder out = new StringBuilder();

    static void solve(int r, int c, int size) {
        char first = grid[r][c];
        boolean same = true;
        outer:
        for (int i = r; i < r + size; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i][j] != first) { same = false; break outer; }
            }
        }
        if (same) { out.append(first); return; }
        int half = size / 2;
        out.append('(');
        solve(r, c, half);
        solve(r, c + half, half);
        solve(r + half, c, half);
        solve(r + half, c + half, half);
        out.append(')');
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(br.readLine().trim());
        grid = new char[n][];
        for (int i = 0; i < n; i++) grid[i] = br.readLine().trim().toCharArray();
        solve(0, 0, n);
        out.append('\n');
        System.out.print(out);
    }
}