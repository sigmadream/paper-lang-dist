import java.io.*;
import java.util.*;

public class Main {
    static char[][] grid;

    static String solve(int r, int c, int size) {
        char first = grid[r][c];
        boolean same = true;
        for (int i = r; i < r + size && same; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i][j] != first) { same = false; break; }
            }
        }
        if (same) return String.valueOf(first);
        int half = size / 2;
        return "(" + solve(r, c, half) + solve(r, c + half, half)
                + solve(r + half, c, half) + solve(r + half, c + half, half) + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.nextToken();
        int n = (int) st.nval;
        grid = new char[n][];
        for (int i = 0; i < n; i++) grid[i] = br.readLine().trim().toCharArray();
        System.out.println(solve(0, 0, n));
    }
}