import java.io.*;
import java.util.*;

public class Main {
    static List<String> grid = new ArrayList<>();

    static String solve(int r, int c, int size) {
        char first = grid.get(r).charAt(c);
        boolean same = true;

        for (int i = r; i < r + size && same; ++i) {
            for (int j = c; j < c + size; ++j) {
                if (grid.get(i).charAt(j) != first) {
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

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line);
        for (int i = 0; i < n; ++i) {
            grid.add(br.readLine().trim());
        }

        StringBuilder sb = new StringBuilder(solve(0, 0, n));
        sb.append('\n');
        System.out.print(sb);
    }
}