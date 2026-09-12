import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Hanoi {
    private static List<String> moves = new ArrayList<>();

    public static void hanoi(int n, int start, int mid, int end) {
        if (n == 1) {
            moves.add(start + " " + end);
            return;
        }
        hanoi(n - 1, start, end, mid);
        moves.add(start + " " + end);
        hanoi(n - 1, mid, start, end);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        hanoi(n, 1, 2, 3);
        System.out.println(moves.size());
        for (String move : moves) {
            System.out.println(move);
        }
    }
}
