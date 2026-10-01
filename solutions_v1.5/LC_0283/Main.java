import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = reader.readLine();
        if (line == null) return;
        StringTokenizer tokenizer = new StringTokenizer(line);
        while (!tokenizer.hasMoreTokens()) {
            line = reader.readLine();
            if (line == null) return;
            tokenizer = new StringTokenizer(line);
        }
        int n = Integer.parseInt(tokenizer.nextToken());
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            while (!tokenizer.hasMoreTokens()) {
                line = reader.readLine();
                if (line == null) break;
                tokenizer = new StringTokenizer(line);
            }
            a[i] = Long.parseLong(tokenizer.nextToken());
        }
        int writeIdx = 0;
        for (int readIdx = 0; readIdx < n; readIdx++) {
            if (a[readIdx] != 0) {
                long temp = a[writeIdx];
                a[writeIdx] = a[readIdx];
                a[readIdx] = temp;
                writeIdx++;
            }
        }
        PrintWriter writer = new PrintWriter(System.out);
        for (int i = 0; i < n; i++) {
            if (i > 0) writer.print(' ');
            writer.print(a[i]);
        }
        writer.println();
        writer.flush();
    }
}
