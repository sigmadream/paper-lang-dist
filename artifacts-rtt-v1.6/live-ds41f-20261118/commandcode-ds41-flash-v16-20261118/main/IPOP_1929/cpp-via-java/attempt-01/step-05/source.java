import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());

        boolean[] isPrime = new boolean[n + 1];
        if (n >= 0) {
            for (int i = 2; i <= n; i++) isPrime[i] = true;
        }

        for (int i = 2; (long) i * i <= n; i++) {
            if (isPrime[i]) {
                for (long j = (long) i * i; j <= n; j += i) {
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