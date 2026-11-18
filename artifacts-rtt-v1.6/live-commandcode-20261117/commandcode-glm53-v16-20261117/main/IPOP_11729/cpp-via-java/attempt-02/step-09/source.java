import java.io.*;

public class Main {
    static StringBuilder moves = new StringBuilder();

    static void hanoi(int n, int start, int mid, int end) {
        if (n == 1) {
            moves.append(start).append(' ').append(end).append('\n');
            return;
        }
        hanoi(n - 1, start, end, mid);
        moves.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) return;
        String t = s.trim();
        if (t.isEmpty()) return;
        int n;
        try {
            n = Integer.parseInt(t);
        } catch (NumberFormatException e) {
            return;
        }
        hanoi(n, 1, 2, 3);
        long count = (1L << n) - 1;
        StringBuilder out = new StringBuilder();
        out.append(count).append('\n').append(moves);
        System.out.print(out);
    }
}