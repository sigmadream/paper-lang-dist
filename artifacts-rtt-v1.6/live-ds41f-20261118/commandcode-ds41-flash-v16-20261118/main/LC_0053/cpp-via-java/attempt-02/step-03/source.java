import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n = sc.nextInt();

        long cur = 0, best = Long.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            long x = sc.nextLong();
            if (i == 0) {
                cur = x;
                best = x;
            } else {
                cur = Math.max(x, cur + x);
                best = Math.max(best, cur);
            }
        }
        System.out.println(best);
    }
}