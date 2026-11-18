import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UncheckedIOException;

public class Main {
    static int N;
    static char[][] grid;

    static String solve(int r, int c, int size) {
        char first = grid[r][c];
        boolean same = true;

        for (int i = r; i < r + size && same; ++i) {
            for (int j = c; j < c + size; ++j) {
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

    public static void main(String[] args) {
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            String line = br.readLine();
            if (line == null) return;

            line = line.trim();
            if (line.isEmpty()) return;

            N = Integer.parseInt(line);

            grid = new char[N][];
            for (int i = 0; i < N; ++i) {
                String row = br.readLine();
                while (row != null && row.isEmpty()) {
                    row = br.readLine();
                }
                if (row == null) return;
                grid[i] = row.trim().toCharArray();
            }

            System.out.println(solve(0, 0, N));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}