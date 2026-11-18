import java.util.Scanner;

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

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            return;
        }
        int n = sc.nextInt();
        int moves = (1 << n) - 1;
        sb.append(moves).append('\n');
        hanoi(n, 1, 2, 3);
        System.out.print(sb.toString());
    }
}