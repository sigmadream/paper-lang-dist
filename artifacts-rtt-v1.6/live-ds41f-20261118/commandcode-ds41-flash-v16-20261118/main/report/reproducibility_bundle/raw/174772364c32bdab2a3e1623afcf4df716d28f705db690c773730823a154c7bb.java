import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String firstLine = br.readLine();
        if (firstLine == null) return;
        firstLine = firstLine.trim();
        if (firstLine.isEmpty()) return;
        int n;
        try {
            n = Integer.parseInt(firstLine.split("\\s+")[0]);
        } catch (NumberFormatException e) {
            return;
        }

        int[] a = new int[n];
        int count = 0;
        while (count < n) {
            String line = br.readLine();
            if (line == null) break;
            StringTokenizer st = new StringTokenizer(line);
            while (st.hasMoreTokens() && count < n) {
                try {
                    a[count] = Integer.parseInt(st.nextToken());
                } catch (NumberFormatException e) {
                    a[count] = 0;
                }
                count++;
            }
        }
        while (count < n) {
            a[count] = 0;
            count++;
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
        System.out.print(sb.toString());
    }
}