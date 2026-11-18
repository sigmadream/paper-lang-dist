import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        if (!sc.hasNextLong()) {
            return;
        }

        long n = sc.nextLong();
        int capacity = n > 0 ? (int) n : 0;
        long[] a = new long[capacity];
        int size = 0;

        while (size < capacity && sc.hasNextLong()) {
            a[size] = sc.nextLong();
            ++size;
        }

        int write = 0;
        for (int read = 0; read < size; ++read) {
            if (a[read] != 0) {
                long tmp = a[write];
                a[write] = a[read];
                a[read] = tmp;
                ++write;
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < size; ++i) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(a[i]);
        }
        sb.append('\n');
        System.out.print(sb.toString());
    }
}