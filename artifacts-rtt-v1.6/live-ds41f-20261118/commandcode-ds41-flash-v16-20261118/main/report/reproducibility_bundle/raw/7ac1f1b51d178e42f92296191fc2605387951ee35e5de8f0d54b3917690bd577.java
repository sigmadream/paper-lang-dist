import java.io.*;

public class Main {
    static void hanoi(int n, int start, int mid, int end, StringBuilder out) {
        if (n == 1) {
            out.append(start).append(' ').append(end).append('\n');
            return;
        }

        hanoi(n - 1, start, end, mid, out);
        out.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end, out);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        line = line.trim();
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line);
        long count = (1L << n) - 1;

        StringBuilder out = new StringBuilder((int) Math.min(Integer.MAX_VALUE, count * 4 + 32));
        out.append(count).append('\n');

        hanoi(n, 1, 2, 3, out);

        System.out.print(out);
    }
}