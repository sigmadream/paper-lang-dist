import java.util.Scanner;

public class Main {
    static int gcdInt(int a, int b) {
        while (b != 0) {
            int r = a % b;
            a = b;
            b = r;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int a = sc.nextInt();
        if (!sc.hasNextInt()) return;
        int b = sc.nextInt();

        int g = gcdInt(a, b);
        System.out.println(g);
        System.out.println((long)(a / g) * b);
    }
}