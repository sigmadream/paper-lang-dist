import java.util.Scanner;

public class Main {
    private static void hanoi(int n, int from, int aux, int to, StringBuilder sb) {
        if (n == 1) {
            sb.append(from).append(" ").append(to).append("\n");
            return;
        }
        hanoi(n - 1, from, to, aux, sb);
        sb.append(from).append(" ").append(to).append("\n");
        hanoi(n - 1, aux, from, to, sb);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            sc.close();
            return;
        }
        int n = sc.nextInt();
        sc.close();
        if (n < 1 || n > 20) {
            return;
        }
        int count = (1 << n) - 1;
        StringBuilder sb = new StringBuilder();
        sb.append(count).append("\n");
        hanoi(n, 1, 2, 3, sb);
        System.out.print(sb);
    }
}