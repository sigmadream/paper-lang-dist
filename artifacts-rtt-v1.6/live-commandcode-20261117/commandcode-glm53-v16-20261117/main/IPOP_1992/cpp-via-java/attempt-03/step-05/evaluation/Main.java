import java.io.*;
import java.util.*;

public class Main {
    static int n;
    static char[][] grid;
    static StringBuilder sb = new StringBuilder();

    static void solve(int r, int c, int size) {
        char first = grid[r][c];
        boolean same = true;
        outer:
        for (int i = r; i < r + size; i++)
            for (int j = c; j < c + size; j++)
                if (grid[i][j] != first) { same = false; break outer; }
        if (same) { sb.append(first); return; }
        int half = size / 2;
        sb.append('(');
        solve(r, c, half);
        solve(r, c + half, half);
        solve(r + half, c, half);
        solve(r + half, c + half, half);
        sb.append(')');
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars('0', '9');
        st.wordChars('0', '9');
        st.nextToken();
        if (st.ttype == StreamTokenizer.TT_EOF) return;
        n = (int) st.nval;
        grid = new char[n][];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            String line = st.sval;
            if (line == null) line = "";
            grid[i] = line.toCharArray();
        }
        solve(0, 0, n);
        sb.append('\n');
        System.out.print(sb);
    }
}