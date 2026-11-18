import java.io.*;
import java.util.*;

public class Main {
    static String[] grid;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String line = br.readLine();
        if (line == null) return;

        while (!line.isEmpty() && (line.charAt(line.length() - 1) == '\r' || line.charAt(line.length() - 1) == '\n')) {
            line = line.substring(0, line.length() - 1);
        }

        if (line.isEmpty()) return;

        int n = Integer.parseInt(line.trim());
        grid = new String[n];

        for (int i = 0; i < n; ++i) {
            String s = br.readLine();
            s = s.replace("\r", "").replace("\n", "");
            grid[i] = s;
        }

        System.out.println(solve(0, 0, n));
    }

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
        String tl = solve(r, c, half);
        String tr = solve(r, c + half, half);
        String bl = solve(r + half, c, half);
        String br = solve(r + half, c + half, half);

        return "(" + tl + tr + bl + br + ")";
    }
}