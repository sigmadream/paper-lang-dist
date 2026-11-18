import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int M = sc.nextInt();
        int N = sc.nextInt();

        boolean[] isPrime = new boolean[N + 1];
        for (int i = 0; i <= N; i++) isPrime[i] = true;
        if (N >= 0) isPrime[0] = false;
        if (N >= 1) isPrime[1] = false;

        for (int i = 2; (long) i * i <= N; i++) {
            if (isPrime[i]) {
                for (long j = (long) i * i; j <= N; j += i) {
                    isPrime[(int) j] = false;
                }
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = M; i <= N; i++) {
            if (isPrime[i]) {
                sb.append(i).append('\n');
            }
        }
        System.out.print(sb);
    }
}