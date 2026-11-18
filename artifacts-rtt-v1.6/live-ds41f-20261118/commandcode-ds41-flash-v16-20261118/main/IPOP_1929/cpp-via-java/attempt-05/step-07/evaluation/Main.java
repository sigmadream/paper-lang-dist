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
        for (int i = 0; i <= n; i++) {
            isPrime[i] = true;
        }

        if (n >= 0) isPrime[0] = false;
        if (n >= 1) isPrime[1] = false;

        for (long longI = 2; longI * longI <= n; longI++) {
            int i = (int) longI;
            if (isPrime[i]) {
                for (long j = longI * longI; j <= n; j += longI) {
                    isPrime[(int) j] = false;
                }
            }
        }

        StringBuilder output = new StringBuilder();
        for (int i = m; i <= n; i++) {
            if (isPrime[i]) {
                output.append(i).append('\n');
            }
        }

        System.out.print(output);
    }
}