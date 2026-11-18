import java.io.*;

public class Main {
    static StringBuilder sb = new StringBuilder();

    static void hanoi(int n, int start, int mid, int end) {
        if (n == 1) {
            sb.append(start).append(' ').append(end).append('\n');
            return;
        }
        hanoi(n - 1, start, end, mid);
        sb.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null || s.trim().isEmpty()) return;
        int n = Integer.parseInt(s.trim());
        hanoi(n, 1, 2, 3);
        long count = (1L << n) - 1;
        StringBuilder out = new StringBuilder();
        out.append(count).append('\n').append(sb);
        System.out.print(out);
    }
}