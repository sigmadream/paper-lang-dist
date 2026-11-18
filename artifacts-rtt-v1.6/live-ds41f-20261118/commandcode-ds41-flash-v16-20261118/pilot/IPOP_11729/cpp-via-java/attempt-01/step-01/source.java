import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    private static void hanoi(int n, int start, int mid, int end, StringBuilder sb) {
        if (n == 1) {
            sb.append((char) ('0' + start)).append(' ')
              .append((char) ('0' + end)).append('\n');
            return;
        }

        hanoi(n - 1, start, end, mid, sb);
        sb.append((char) ('0' + start)).append(' ')
          .append((char) ('0' + end)).append('\n');
        hanoi(n - 1, mid, start, end, sb);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        int n = Integer.parseInt(line.trim());
        int moves = (1 << n) - 1;

        StringBuilder sb = new StringBuilder(4 * moves + 16);
        sb.append(moves).append('\n');
        hanoi(n, 1, 2, 3, sb);

        System.out.print(sb);
    }
}