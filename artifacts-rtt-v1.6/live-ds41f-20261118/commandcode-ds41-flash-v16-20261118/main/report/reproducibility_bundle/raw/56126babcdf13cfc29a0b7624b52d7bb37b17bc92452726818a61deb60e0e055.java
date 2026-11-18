import java.util.Scanner;

public class Main {
    static void hanoi(int n, int start, int mid, int end, StringBuilder sb) {
        if (n == 1) {
            sb.append(start).append(' ').append(end).append('\n');
            return;
        }
        hanoi(n - 1, start, end, mid, sb);
        sb.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end, sb);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            return;
        }

        int n = sc.nextInt();

        StringBuilder sb = new StringBuilder();
        sb.append((1L << n) - 1).append('\n');
        hanoi(n, 1, 2, 3, sb);

        System.out.print(sb);
    }
}