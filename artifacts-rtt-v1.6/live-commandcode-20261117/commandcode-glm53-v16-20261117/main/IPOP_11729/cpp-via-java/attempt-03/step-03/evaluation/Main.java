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
        String line = br.readLine();
        if (line == null) return;
        int n = Integer.parseInt(line.trim());
        hanoi(n, 1, 2, 3);
        long count = (1L << n) - 1;
        StringBuilder sb = new StringBuilder();
        sb.append(count).append('\n').append(moves);
        System.out.print(sb);
    }
}