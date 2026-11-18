import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 256);
        st.wordChars('0', '9');
        st.whitespaceChars(0, ' ');
        st.whitespaceChars('\n', '\r');
        st.whitespaceChars('\t', '\t');
        st.eolIsSignificant(false);
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) Double.parseDouble(st.sval);
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            a[i] = Long.parseLong(st.sval);
        }
        long cur = a[0], best = a[0];
        for (int i = 1; i < n; i++) {
            cur = Math.max(a[i], cur + a[i]);
            best = Math.max(best, cur);
        }
        System.out.println(best);
    }
}