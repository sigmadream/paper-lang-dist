import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int n = Integer.parseInt(line.trim());
        int[] counts = new int[n + 1];
        for (int i = 1; i <= n; i++) counts[i] = counts[i / 2] + i % 2;
        StringBuilder out = new StringBuilder();
        for (int i = 0; i <= n; i++) {
            if (i > 0) out.append(' ');
            out.append(counts[i]);
        }
        out.append('\n');
        System.out.print(out);
    }
}