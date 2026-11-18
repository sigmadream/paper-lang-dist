import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        String line = br.readLine();
        if (line == null) return;

        int n;
        try {
            n = Integer.parseInt(line.trim());
        } catch (NumberFormatException e) {
            return;
        }

        int[] a = new int[n];
        int count = 0;
        StringBuilder input = new StringBuilder(line);
        while (count < n) {
            String nextLine = br.readLine();
            if (nextLine == null) break;
            input.append(' ').append(nextLine);
        }

        StringTokenizer st = new StringTokenizer(input.toString());
        // Skip the first token, which is n
        if (st.hasMoreTokens()) st.nextToken();
        for (int i = 0; i < n; ++i) {
            if (st.hasMoreTokens()) {
                try {
                    a[i] = Integer.parseInt(st.nextToken());
                } catch (NumberFormatException e) {
                    a[i] = 0;
                }
            } else {
                a[i] = 0;
            }
        }

        int write = 0;
        for (int read = 0; read < n; ++read) {
            if (a[read] != 0) {
                int tmp = a[write];
                a[write] = a[read];
                a[read] = tmp;
                ++write;
            }
        }

        for (int i = 0; i < n; ++i) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        sb.append('\n');
        System.out.print(sb);
    }
}