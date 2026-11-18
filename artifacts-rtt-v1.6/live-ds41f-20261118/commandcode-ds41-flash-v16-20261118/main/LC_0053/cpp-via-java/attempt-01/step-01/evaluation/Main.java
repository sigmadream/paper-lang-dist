import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        long cur = sc.nextLong();
        long best = cur;

        for (int i = 1; i < n; i++) {
            long x = sc.nextLong();
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}