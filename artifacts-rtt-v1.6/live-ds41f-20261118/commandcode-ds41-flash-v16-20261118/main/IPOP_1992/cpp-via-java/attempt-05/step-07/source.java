import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    static String[] grid;

    static String solve(int r, int c, int size) {
        char first = grid[r].charAt(c);
        boolean same = true;
        outer:
        for (int i = r; i < r + size; ++i) {
            for (int j = c; j < c + size; ++j) {
                if (grid[i].charAt(j) != first) {
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
        String line = br.readLine();
        if (line == null) return;
        line = line.replace("\r", "").trim();
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line);
        grid = new String[n];

        for (int i = 0; i < n; ++i) {
            String s = br.readLine();
            if (s == null) s = "";
            s = s.replace("\r", "").trim();
            grid[i] = s;
        }

        System.out.println(solve(0, 0, n));
    }
}