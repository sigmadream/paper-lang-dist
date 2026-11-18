import java.util.Scanner;

public class Main {
    static void hanoi(int n, int start, int mid, int end, StringBuilder out) {
        if (n == 1) {
            out.append(start).append(' ').append(end).append('\n');
            return;
        }
        hanoi(n - 1, start, end, mid, out);
        out.append(start).append(' ').append(end).append('\n');
        hanoi(n - 1, mid, start, end, out);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        sc.close();

        int moves = (1 << n) - 1;
        StringBuilder output = new StringBuilder();
        output.append(moves).append('\n');
        hanoi(n, 1, 2, 3, output);
        System.out.print(output);
    }
}