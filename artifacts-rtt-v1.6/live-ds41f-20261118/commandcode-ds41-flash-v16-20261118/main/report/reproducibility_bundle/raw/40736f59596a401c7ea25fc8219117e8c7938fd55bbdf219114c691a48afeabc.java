import java.io.*;

public class Main {
    private static String[] grid;
    private static int n;

    private static String solve(int r, int c, int size) {
        char first = grid[r].charAt(c);
        boolean same = true;

        for (int i = r; i < r + size && same; i++) {
            for (int j = c; j < c + size; j++) {
                if (grid[i].charAt(j) != first) {
                    same = false;
                    break;
                }
            }
        }

        if (same) return String.valueOf(first);

        int half = size / 2;
        StringBuilder result = new StringBuilder();
        result.append('(');
        result.append(solve(r, c, half));
        result.append(solve(r, c + half, half));
        result.append(solve(r + half, c, half));
        result.append(solve(r + half, c + half, half));
        result.append(')');
        return result.toString();
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String line = br.readLine();
        if (line == null) return;

        line = line.trim();
        if (line.isEmpty()) return;

        n = Integer.parseInt(line);
        grid = new String[n];

        int row = 0;
        while (row < n && (line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;

            grid[row] = line;
            row++;
        }

        System.out.println(solve(0, 0, n));
    }
}