import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 256);
        st.wordChars('0', '9');
        st.whitespaceChars(' ', '\n');
        st.eolIsSignificant(false);

        st.nextToken(); int n = (int) st.nval;
        st.nextToken(); int c = (int) st.nval;

        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            a[i] = (long) st.nval;
        }

        Arrays.sort(a);

        long l = 1, r = a[n - 1] - a[0], ans = 0;
        while (l <= r) {
            long mid = l + (r - l) / 2;
            int count = 1;
            long prev = a[0];
            for (int i = 1; i < n; i++) {
                if (a[i] - prev >= mid) {
                    count++;
                    prev = a[i];
                }
            }
            if (count >= c) {
                ans = mid;
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }

        System.out.println(ans);
    }
}