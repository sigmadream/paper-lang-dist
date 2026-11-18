import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] parts = br.readLine().trim().split("\\s+");
        int m = Integer.parseInt(parts[0]);
        int n = Integer.parseInt(parts[1]);

        boolean[] isPrime = new boolean[n + 1];
        java.util.Arrays.fill(isPrime, true);
        if (n >= 0) isPrime[0] = false;
        if (n >= 1) isPrime[1] = false;

        for (long i = 2; i * i <= n; i++) {
            int idx = (int) i;
            if (isPrime[idx]) {
                for (long j = i * i; j <= n; j += i) {
                    isPrime[(int) j] = false;
                }
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = m; i <= n; i++) {
            if (isPrime[i]) {
                sb.append(i).append('\n');
            }
        }
        System.out.print(sb);
    }
}