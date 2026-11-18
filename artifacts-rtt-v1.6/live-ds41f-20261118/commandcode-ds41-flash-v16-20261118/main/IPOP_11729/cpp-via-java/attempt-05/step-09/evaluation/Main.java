import java.io.*;

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
        int n = Integer.parseInt(br.readLine().trim());

        long count = (1L << n) - 1;
        output.ensureCapacity((int) (count * 8 + 32));

        output.append(count).append('\n');
        hanoi(n, 1, 2, 3);

        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        bw.append(output);
        bw.flush();
    }
}