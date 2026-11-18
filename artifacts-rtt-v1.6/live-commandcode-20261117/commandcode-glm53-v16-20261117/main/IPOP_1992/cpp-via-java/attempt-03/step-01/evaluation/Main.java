import java.io.*;
import java.util.*;

public class Main {
    static char[][] grid;
    static int n;

    static String solve(int r, int c, int size) {
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
        String tl = solve(r, c, half);
        String tr = solve(r, c + half, half);
        String bl = solve(r + half, c, half);
        String br = solve(r + half, c + half, half);
        return "(" + tl + tr + bl + br + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumbers();
        st.nextToken();
        n = (int) st.nval;
        if (n <= 0) return;
        grid = new char[n][];
        for (int i = 0; i < n; i++) {
            String line = br.readLine();
            while (line != null && line.trim().isEmpty()) line = br.readLine();
            if (line == null) break;
            grid[i] = line.trim().toCharArray();
        }
        StringBuilder sb = new StringBuilder();
        sb.append(solve(0, 0, n)).append('\n');
        System.out.print(sb);
    }
}