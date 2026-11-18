import java.util.*;
import java.io.*;

public class Main {
    static String[] grid;
    
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
        String tl = solve(r, c, half);
        String tr = solve(r, c + half, half);
        String bl = solve(r + half, c, half);
        String br = solve(r + half, c + half, half);
        
        return "(" + tl + tr + bl + br + ")";
    }
    
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) return;
        int n = Integer.parseInt(line.trim());
        grid = new String[n];
        for (int i = 0; i < n; i++) {
            grid[i] = br.readLine().trim();
        }
        sb.append(solve(0, 0, n)).append("\n");
        System.out.print(sb.toString());
    }
}