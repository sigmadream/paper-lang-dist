import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        int start = 0;
        int end = line.length() - 1;
        while (start <= end && (line.charAt(start) == ' ' || line.charAt(start) == '\t'
                || line.charAt(start) == '\r' || line.charAt(start) == '\n')) {
            start++;
        }
        if (start > end) return;
        while (end >= start && (line.charAt(end) == ' ' || line.charAt(end) == '\t'
                || line.charAt(end) == '\r' || line.charAt(end) == '\n')) {
            end--;
        }
        String trimmed = line.substring(start, end + 1);
        if (trimmed.isEmpty()) return;

        int n;
        try {
            n = Integer.parseInt(trimmed);
        } catch (NumberFormatException e) {
            return;
        }
        if (n < 0) return;

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

        System.out.print(sb.toString());
    }
}