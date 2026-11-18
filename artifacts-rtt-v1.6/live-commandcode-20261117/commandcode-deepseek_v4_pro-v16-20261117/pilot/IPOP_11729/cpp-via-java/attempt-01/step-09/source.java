import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            return;
        }
        int n = sc.nextInt();
        if (n < 1 || n > 20) {
            return;
        }
        long moves = (1L << n) - 1;
        StringBuilder out = new StringBuilder();
        out.append(moves).append('\n');
        hanoi(n, 1, 2, 3, out);
        System.out.print(out);
    }

    private static void hanoi(int n, int from, int aux, int to, StringBuilder out) {
        if (n == 1) {
            out.append(from).append(' ').append(to).append('\n');
            return;
        }
        hanoi(n - 1, from, to, aux, out);
        out.append(from).append(' ').append(to).append('\n');
        hanoi(n - 1, aux, from, to, out);
    }
}