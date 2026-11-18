import java.io.IOException;

public class Main {
    private static final StringBuilder output = new StringBuilder();

    private static void hanoi(int n, int start, int mid, int end) {
        if (n == 1) {
            output.append((char) ('0' + start));
            output.append(' ');
            output.append((char) ('0' + end));
            output.append('\n');
            return;
        }

        hanoi(n - 1, start, end, mid);
        output.append((char) ('0' + start));
        output.append(' ');
        output.append((char) ('0' + end));
        output.append('\n');
        hanoi(n - 1, mid, start, end);
    }

    public static void main(String[] args) throws IOException {
        int n = System.in.read() - '0';
        int next;
        while ((next = System.in.read()) >= '0' && next <= '9') {
            n = n * 10 + (next - '0');
        }

        long count = (1L << n) - 1;

        output.append(count);
        output.append('\n');

        hanoi(n, 1, 2, 3);

        System.out.print(output);
    }
}