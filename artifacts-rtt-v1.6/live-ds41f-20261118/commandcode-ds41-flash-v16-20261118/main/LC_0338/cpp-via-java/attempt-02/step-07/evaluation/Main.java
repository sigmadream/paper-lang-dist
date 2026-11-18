import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        String trimmed = line.trim();
        if (trimmed.isEmpty()) return;

        int n;
        try {
            n = Integer.parseInt(trimmed);
        } catch (NumberFormatException e) {
            return;
        }

        int[] counts = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            counts[i] = counts[i / 2] + (i % 2);
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(counts[i]);
        }
        sb.append('\n');

        System.out.print(sb);
    }
}