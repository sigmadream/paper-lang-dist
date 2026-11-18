import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static char[][] grid;
    static StringBuilder sb = new StringBuilder();

    static void solve(int r, int c, int size) {
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

        if (same) {
            sb.append(first);
            return;
        }

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
        String line = br.readLine();
        if (line == null) return;
        int n = Integer.parseInt(line.trim());

        grid = new char[n][];
        for (int i = 0; i < n; i++) {
            grid[i] = br.readLine().toCharArray();
        }

        solve(0, 0, n);
        System.out.println(sb.toString());
    }
}