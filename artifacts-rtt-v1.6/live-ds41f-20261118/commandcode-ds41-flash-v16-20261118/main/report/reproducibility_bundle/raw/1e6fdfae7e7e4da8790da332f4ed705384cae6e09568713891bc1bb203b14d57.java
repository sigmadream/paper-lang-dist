import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static final StringBuilder output = new StringBuilder();

    private static void hanoi(int n, int start, int mid, int end) {
        if (n == 1) {
            output.append(start).append(' ').append(end).append('\n');
            return;
        }

        hanoi(n - 1, start, end, mid);
        output.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null || line.isEmpty()) {
            return;
        }

        int n = Integer.parseInt(line.trim());
        long count = (1L << n) - 1;

        output.ensureCapacity((1 << n) * 4 + 32);
        output.append(count).append('\n');

        hanoi(n, 1, 2, 3);

        System.out.print(output);
    }
}