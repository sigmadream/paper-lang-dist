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
        StringBuilder sb = new StringBuilder();
        sb.append(moves).append('\n');
        hanoi(n, 1, 2, 3, sb);
        System.out.print(sb);
    }

    static void hanoi(int n, int from, int aux, int to, StringBuilder sb) {
        if (n == 1) {
            sb.append(from).append(' ').append(to).append('\n');
            return;
        }
        hanoi(n - 1, from, to, aux, sb);
        sb.append(from).append(' ').append(to).append('\n');
        hanoi(n - 1, aux, from, to, sb);
    }
}