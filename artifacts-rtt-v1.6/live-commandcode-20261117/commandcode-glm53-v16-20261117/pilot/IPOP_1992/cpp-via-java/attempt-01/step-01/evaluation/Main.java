import java.io.*;
import java.util.*;

public class Main {
    static char[][] grid;
    static int n;

    static StringBuilder solve(int r, int c, int size) {
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
        StringBuilder sb = new StringBuilder();
        if (same) {
            sb.append(first);
            return sb;
        }
        int half = size / 2;
        sb.append('(');
        sb.append(solve(r, c, half));
        sb.append(solve(r, c + half, half));
        sb.append(solve(r + half, c, half));
        sb.append(solve(r + half, c + half, half));
        sb.append(')');
        return sb;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumbers();
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        n = (int) st.nval;
        grid = new char[n][];
        for (int i = 0; i < n; i++) {
            String line = br.readLine();
            while (line != null && line.trim().isEmpty()) line = br.readLine();
            if (line == null) return;
            grid[i] = line.trim().toCharArray();
        }
        StringBuilder sb = solve(0, 0, n);
        System.out.println(sb);
    }
}