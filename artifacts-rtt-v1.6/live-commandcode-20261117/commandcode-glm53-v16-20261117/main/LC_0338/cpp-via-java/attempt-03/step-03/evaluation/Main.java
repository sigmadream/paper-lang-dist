import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) return;
        int n = Integer.parseInt(line.trim());
        int[] counts = new int[n + 1];
        StringBuilder s = new StringBuilder();
        for (int i = 0; i <= n; i++) {
            if (i > 0) counts[i] = counts[i / 2] + (i % 2);
            if (i > 0) s.append(' ');
            s.append(counts[i]);
        }
        s.append('\n');
        System.out.print(s);
    }
}