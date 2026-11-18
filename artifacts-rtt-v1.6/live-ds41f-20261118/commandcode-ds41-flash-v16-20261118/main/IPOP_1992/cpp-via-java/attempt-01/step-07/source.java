import java.io.*;

public class Main {
    static String[] grid;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        if (line.endsWith("\r")) line = line.substring(0, line.length() - 1);
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line.trim());
        grid = new String[n];
        for (int i = 0; i < n; i++) {
            String s = br.readLine();
            if (s == null) s = "";
            if (s.endsWith("\r")) s = s.substring(0, s.length() - 1);
            grid[i] = s;
        }

        System.out.println(solve(0, 0, n));
    }

    static String solve(int r, int c, int size) {
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
        StringBuilder sb = new StringBuilder();
        sb.append('(');
        sb.append(solve(r, c, half));
        sb.append(solve(r, c + half, half));
        sb.append(solve(r + half, c, half));
        sb.append(solve(r + half, c + half, half));
        sb.append(')');
        return sb.toString();
    }
}