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
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) return;
        int n = Integer.parseInt(line.trim());
        sb.append((1L << n) - 1).append('\n');
        hanoi(n, 1, 2, 3);
        System.out.print(sb);
    }
}