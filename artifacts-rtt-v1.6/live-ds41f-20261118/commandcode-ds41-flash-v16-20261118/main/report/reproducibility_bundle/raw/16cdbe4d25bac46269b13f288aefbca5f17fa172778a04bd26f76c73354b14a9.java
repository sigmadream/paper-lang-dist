import java.io.*;

public class Main {
    static int N;
    static String[] grid;
    static StringBuilder sb = new StringBuilder();

    static boolean isSame(int r, int c, int size) {
        char first = grid[r].charAt(c);
        for (int i = r; i < r + size; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i].charAt(j) != first) {
                    return false;
                }
            }
        }
        return true;
    }

    static void solve(int r, int c, int size) {
        if (isSame(r, c, size)) {
            sb.append(grid[r].charAt(c));
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

        N = Integer.parseInt(line.trim());
        grid = new String[N];
        for (int i = 0; i < N; i++) {
            grid[i] = br.readLine().trim();
        }

        solve(0, 0, N);
        System.out.println(sb.toString());
    }
}