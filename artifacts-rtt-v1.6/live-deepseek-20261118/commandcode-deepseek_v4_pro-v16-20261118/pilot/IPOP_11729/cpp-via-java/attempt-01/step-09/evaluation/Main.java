import java.io.*;

public class Main {
    static StringBuilder sb = new StringBuilder();

    static void hanoi(int n, int from, int aux, int to) {
        if (n == 1) {
            sb.append(from).append(' ').append(to).append('\n');
            return;
        }
        hanoi(n - 1, from, to, aux);
        sb.append(from).append(' ').append(to).append('\n');
        hanoi(n - 1, aux, from, to);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());

        int moves = (1 << n) - 1;
        sb.append(moves).append('\n');

        hanoi(n, 1, 2, 3);

        System.out.print(sb);
    }
}