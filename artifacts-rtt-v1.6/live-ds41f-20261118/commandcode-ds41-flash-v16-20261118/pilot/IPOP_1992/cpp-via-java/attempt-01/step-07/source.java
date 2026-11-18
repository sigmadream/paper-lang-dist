import java.io.*;

public class Main {
    static int N;
    static String[] grid;

    static String solve(int r, int c, int size) {
        char first = grid[r].charAt(c);
        boolean same = true;

        for (int i = r; i < r + size && same; ++i) {
            for (int j = c; j < c + size; ++j) {
                if (grid[i].charAt(j) != first) {
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
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;
        N = Integer.parseInt(line);
        grid = new String[N];
        for (int i = 0; i < N; ++i) {
            grid[i] = br.readLine().trim();
        }

        StringBuilder out = new StringBuilder();
        out.append(solve(0, 0, N));
        out.append('\n');
        System.out.print(out.toString());
    }
}