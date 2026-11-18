import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        StreamTokenizer st = new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in)));
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) st.nval;

        st.nextToken();
        long x = (long) st.nval;

        long cur = x;
        long best = x;

        for (int i = 1; i < n; ++i) {
            st.nextToken();
            x = (long) st.nval;
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}