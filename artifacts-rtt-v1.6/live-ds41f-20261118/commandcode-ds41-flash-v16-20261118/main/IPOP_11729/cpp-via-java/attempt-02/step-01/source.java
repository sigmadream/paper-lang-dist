import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

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
        if (line == null) return;

        line = line.trim();
        if (line.isEmpty()) return;

        int n = Integer.parseInt(line);
        int count = (1 << n) - 1;

        sb.append(count).append('\n');
        hanoi(n, 1, 2, 3);

        System.out.print(sb);
    }
}