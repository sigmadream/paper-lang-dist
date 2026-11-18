import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    private static void hanoi(int n, int start, int mid, int end, StringBuilder sb) {
        if (n == 1) {
            sb.append(start).append(' ').append(end).append('\n');
            return;
        }
        hanoi(n - 1, start, end, mid, sb);
        sb.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end, sb);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) {
            return;
        }

        int n = Integer.parseInt(line.trim());
        StringBuilder sb = new StringBuilder();
        sb.append((1 << n) - 1).append('\n');
        hanoi(n, 1, 2, 3, sb);
        System.out.print(sb);
    }
}