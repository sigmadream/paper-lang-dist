import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    private static StringBuilder output;

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
        if (line == null) return;

        line = line.trim();
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line);
        int count = (1 << n) - 1;

        output = new StringBuilder(count * 5 + 16);
        output.append(count).append('\n');

        hanoi(n, 1, 2, 3);

        System.out.print(output);
    }
}