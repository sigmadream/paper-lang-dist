import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 256);
        st.wordChars(33, 126);
        st.whitespaceChars(0, ' ');
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int m = Integer.parseInt(st.sval);
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = Integer.parseInt(st.sval);

        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        if (n >= 0) isPrime[0] = false;
        if (n >= 1) isPrime[1] = false;

        for (int i = 2; (long) i * i <= n; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= n; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = m; i <= n; i++) {
            if (isPrime[i]) sb.append(i).append('\n');
        }
        System.out.print(sb);
    }
}