import java.io.*;
import java.util.StringTokenizer;

public class Main {
    static StringBuilder out;

    static void appendInt(long x) {
        out.append(x);
    }

    static void hanoi(int n, int start, int mid, int end) {
        if (n == 1) {
            out.append(start).append(' ').append(end).append('\n');
            return;
        }

        hanoi(n - 1, start, end, mid);

        out.append(start).append(' ').append(end).append('\n');

        hanoi(n - 1, mid, start, end);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        StringTokenizer st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;

        int n = Integer.parseInt(st.nextToken());
        long count = (1L << n) - 1;

        out = new StringBuilder((int) (count * 6 + 32));

        appendInt(count);
        out.append('\n');

        hanoi(n, 1, 2, 3);

        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        bw.write(out.toString());
        bw.flush();
    }
}