import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int M = Integer.parseInt(st.nextToken());
        int N = Integer.parseInt(st.nextToken());

        boolean[] isPrime = new boolean[N + 1];
        Arrays.fill(isPrime, true);

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