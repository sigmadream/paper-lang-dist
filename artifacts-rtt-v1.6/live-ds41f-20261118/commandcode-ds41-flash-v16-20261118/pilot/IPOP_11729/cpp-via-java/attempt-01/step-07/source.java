import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static void hanoi(int n, int start, int mid, int end, StringBuilder out) {
        if (n == 1) {
            out.append(start).append(' ').append(end).append('\n');
            return;
        }

        hanoi(n - 1, start, end, mid, out);
        out.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end, out);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();

        if (line == null) {
            return;
        }

        int n = Integer.parseInt(line.trim());
        int moves = (1 << n) - 1;

        StringBuilder out = new StringBuilder(Math.max(16, moves * 4 + 16));
        out.append(moves).append('\n');

        hanoi(n, 1, 2, 3, out);

        System.out.print(out);
    }
}